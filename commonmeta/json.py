"""Various mechanisms for operating on JSON."""

try:
    import msgspec.json

    def loads(obj):
        return msgspec.json.decode(obj)

    def dumps(obj, option=None):
        byte_array = msgspec.json.encode(obj)
        return byte_array.decode()

except ModuleNotFoundError:
    try:
        from orjson import dumps, loads

    except ModuleNotFoundError:
        try:
            from ujson import dumps, loads

        except ModuleNotFoundError:
            from json import dumps, loads

__all__ = ("dumps", "loads")
