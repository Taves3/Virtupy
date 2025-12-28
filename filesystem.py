from __future__ import annotations
from dataclasses import dataclass

@dataclass
class VFileNode:
    data: str = ""

class Environment:
    def __init__(self):
        self.files: dict[str, VFileNode] = {}

    # ---------- path utils ----------
    def _norm(self, path: str) -> str:
        path = path.replace("\\", "/")
        if not path.startswith("/"):
            path = "/" + path
        return path.rstrip("/") or "/"

    # ---------- file ops ----------
    def open(self, path: str, mode: str = "r") -> "VFile":
        path = self._norm(path)

        if "r" in mode and path not in self.files:
            raise FileNotFoundError(path)

        if "w" in mode:
            self.files[path] = VFileNode()

        if "a" in mode:
            self.files.setdefault(path, VFileNode())

        return VFile(self, path, mode)

    def exists(self, path: str) -> bool:
        return self._norm(path) in self.files

    def delete(self, path: str):
        path = self._norm(path)
        if path not in self.files:
            raise FileNotFoundError(path)
        del self.files[path]

    def snapshot(self) -> dict[str, str]:
        # super useful for Virtupy rollback / rewind
        return {k: v.data for k, v in self.files.items()}

    def restore(self, snap: dict[str, str]):
        self.files = {k: VFileNode(v) for k, v in snap.items()}

class VFile:
    def __init__(self, fs: Environment, path: str, mode: str):
        self.fs = fs
        self.path = path
        self.mode = mode
        self.closed = False
        self.pos = 0

        if "a" in mode:
            self.pos = len(self.fs.files[path].data)

    def read(self, size: int = -1) -> str:
        self._check()
        data = self.fs.files[self.path].data

        if size < 0:
            out = data[self.pos :]
            self.pos = len(data)
            return out

        out = data[self.pos : self.pos + size]
        self.pos += size
        return out

    def write(self, text: str) -> int:
        self._check()
        if "r" in self.mode:
            raise IOError("file not writable")

        node = self.fs.files[self.path]
        before = node.data[: self.pos]
        after = node.data[self.pos + len(text) :]
        node.data = before + text + after
        self.pos += len(text)
        return len(text)

    def seek(self, pos: int):
        self._check()
        self.pos = max(0, pos)

    def tell(self) -> int:
        return self.pos

    def close(self):
        self.closed = True

    def _check(self):
        if self.closed:
            raise ValueError("I/O on closed file")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()