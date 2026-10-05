import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import org.apache.nifi.processor.io.StreamCallback
import java.nio.charset.StandardCharsets
import java.time.Instant
import java.time.LocalDateTime
import java.time.ZoneOffset

// NiFi ExecuteScript: one public forecast response -> typed hourly records.
// Reject missing/null/duplicate hours: never manufacture a weather measurement.
def flowFile = session.get()
if (flowFile == null) return
try {
    def records
    def sourceUrl = flowFile.getAttribute('source_url')
    def fetchedAt = flowFile.getAttribute('fetched_at_utc')
    def sourceObject = flowFile.getAttribute('source_object')
    flowFile = session.write(flowFile, { input, output ->
        def payload = new JsonSlurper().parse(input, 'UTF-8')
        if (payload.utc_offset_seconds != 0) throw new IllegalArgumentException('UTC required')
        if (payload.hourly_units.temperature_2m != '°C' || payload.hourly_units.relative_humidity_2m != '%') {
            throw new IllegalArgumentException('Unexpected units')
        }
        def hours = payload.hourly.time
        def temperatures = payload.hourly.temperature_2m
        def humidities = payload.hourly.relative_humidity_2m
        if (!hours || hours.size() != temperatures.size() || hours.size() != humidities.size()) {
            throw new IllegalArgumentException('Hourly arrays differ or are empty')
        }
        if (hours.toSet().size() != hours.size()) throw new IllegalArgumentException('Repeated timestamps')
        records = (0..<hours.size()).collect { index ->
            def temperature = temperatures[index]
            def humidity = humidities[index]
            if (!(temperature instanceof Number) || !(humidity instanceof Number)) {
                throw new IllegalArgumentException('Missing/non-numeric forecast')
            }
            def t = temperature.doubleValue()
            def h = humidity.doubleValue()
            if (!Double.isFinite(t) || !Double.isFinite(h) || h < 0 || h > 100) {
                throw new IllegalArgumentException('Invalid forecast value')
            }
            def instant = LocalDateTime.parse(hours[index]).toInstant(ZoneOffset.UTC)
            [municipio: 'Elche', timestamp_utc: instant.toString(),
             temperatura_c: t, humedad_pct: h,
             provider: 'open-meteo', data_kind: 'modeled_forecast',
             timezone: 'UTC', source_url: sourceUrl,
             fetched_at_utc: fetchedAt, source_object: sourceObject]
        }
        output.write(JsonOutput.toJson(records).getBytes(StandardCharsets.UTF_8))
    } as StreamCallback)
    flowFile = session.putAttribute(flowFile, 'record.count', records.size().toString())
    flowFile = session.putAttribute(flowFile, 'mime.type', 'application/json')
    session.transfer(flowFile, REL_SUCCESS)
} catch (Exception error) {
    log.error('Open-Meteo hourly validation failed', error)
    session.transfer(flowFile, REL_FAILURE)
}
