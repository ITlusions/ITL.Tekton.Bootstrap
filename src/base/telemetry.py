from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter
from opentelemetry import metrics
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_opentelemetry(app: FastAPI):
    # Initialize OpenTelemetry Metrics
    metrics.set_meter_provider(MeterProvider())
    meter = metrics.get_meter(__name__)

    # Set up Prometheus Exporter
    prometheus_exporter = PrometheusMetricsExporter()

    # Export metrics to Prometheus
    meter.add_exporter(prometheus_exporter)

    FastAPIInstrumentor().instrument_app(app)

    # Expose a metrics endpoint for Prometheus to scrape
