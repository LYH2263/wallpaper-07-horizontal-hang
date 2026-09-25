import os
import tempfile

# Isolate the test database before any app module reads DATA_DIR.
os.environ.setdefault("DATA_DIR", tempfile.mkdtemp(prefix="wallpaper-test-"))
