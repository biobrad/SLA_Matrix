import pynecone as pc

config = pc.Config(
    app_name="newmatrix",
    api_url="192.168.10.100:8000",
    bun_path="$HOME/.bun/bin/bun",
    db_url="sqlite:///pynecone.db",
)
