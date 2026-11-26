#!/usr/bin/env python3
r"""
ew_layer_log.py -- turn on The Evil Within's dormant file logger at runtime.

Why this is needed
------------------
Retail constructs idCommonLocal's idLogFileWriter (EvilWithin.exe+0x2258C68)
but never links it into the engine's print-listener list, so the cvars
`logFile`, `logFileName` and `logFile_SystemRunning` do nothing: no
qconsole.log is ever written.  idConsoleLocal::Init is the only caller of
RegisterPrintListener (0x140D47F00) and it registers only the console sink.

This script links the writer into that list with three writes, sets
logFile=2 (write + flush every line) and raises g_debugLayers so the layer
activate / deactivate / change messages are emitted at level 1.

Usage
-----
    python ew_layer_log.py            # enable
    python ew_layer_log.py --check    # show state, change nothing
    python ew_layer_log.py --undo     # unlink the writer, restore flags
    python ew_layer_log.py --off      # only g_debugLayers = 0
    python ew_layer_log.py --dump-layers
    python ew_layer_log.py --dump-layers --prefix st12
    python ew_layer_log.py --dump-entities
    python ew_layer_log.py --dump-entities --prefix trigger

`--dump-layers` reads the live idGameLocal layer registry
(gameLocal+0x318, stride 0xA8, name pointer at +0x08) and prints every layer
name the loaded map knows about, plus a ready-to-paste quoted list.
`--dump-entities` reads the live entity array
(gameLocal+0x68 -> manager, array at +0x28, name at entity+0x08) and prints
the entities that currently exist. Use the two together to find the trigger
that streams a section and the checkpoint/save entity you want to reach,
without walking there.

After enabling, type anything in the in-game console (for example
`g_debugLayers`).  The engine prints that echo at level 1, which makes the
writer create:

    <install>\base\qconsole.log

On a clean exit the writer renames the file to <install>\logs\qconsole.log.
Copy base\qconsole.log while playing if you want to be certain.

Verified against the retail Epic build in this folder.  Everything is
anchored: the script refuses to write if the writer vtable or the listener
list do not look the way the binary says they should.
"""

from __future__ import annotations

import argparse
import ctypes
import re
import struct
import sys
from ctypes import wintypes as wt

# ---------------------------------------------------------------------------
# Addresses (RVA = address - 0x140000000), all verified in EvilWithin.exe
# ---------------------------------------------------------------------------

IMAGE_BASE = 0x140000000

RVA_G_DEBUG_LAYERS = 0x09C5BD18   # cvar value field (int, object+0x28)
RVA_LIST_HEAD      = 0x09C9D2A8   # print-listener list head
RVA_WRITER         = 0x02258C68   # idCommonLocal+8, the idLogFileWriter
RVA_LOG_FILE       = 0x0226BF78   # cvar `logFile` value field
RVA_LOG_FILE_SR    = 0x0226BFF8   # cvar `logFile_SystemRunning` value field

# live layer registry: idGameLocal::gameLocal, then its idList<idLayer> at +0x318
RVA_GAME_LOCAL     = 0x09C58A88
GL_LAYER_LIST      = 0x318        # idList data pointer (+0), count (+8), capacity (+0xc)
GL_LAYER_COUNT     = 0x320
LAYER_ENTRY_STRIDE = 0xA8
LAYER_ENTRY_NAME   = 0x08         # char* to the layer name

# live entity list: idGameLocal+0x68 -> entity manager, array at +0x28
GL_ENTITY_HASH      = 0x68
ENTITY_ARRAY_OFF    = 0x28
ENTITY_NAME_OFF     = 0x08        # char* to the entity name
MAX_GENTITIES       = 0x20000

# fields inside the writer object (base = RVA_WRITER)
WRITER_NEXT      = 0x08   # -> 0x02258C70
WRITER_ENABLED   = 0x10   # -> 0x02258C78  (byte; +0x11 is the thread flag)
WRITER_THRESHOLD = 0x14   # -> 0x02258C7C  (dword, ctor sets 1)
WRITER_FILE      = 0x18   # -> 0x02258C80  (file handle, 0 = not open)
WRITER_OPENING   = 0x20   # -> 0x02258C88  (re-entrancy guard)

# sanity anchors
RVA_WRITER_VTABLE  = 0x01552188   # idLogFileWriter vtable
RVA_CONSOLE_VTABLE = 0x0155B568   # idConsoleLocal log-listener vtable

# ---------------------------------------------------------------------------
# Win32
# ---------------------------------------------------------------------------

TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010

PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_QUERY_INFORMATION = 0x0400

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

k32 = ctypes.WinDLL("kernel32", use_last_error=True)


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wt.DWORD),
        ("cntUsage", wt.DWORD),
        ("th32ProcessID", wt.DWORD),
        ("th32DefaultHeapID", ctypes.c_size_t),
        ("th32ModuleID", wt.DWORD),
        ("cntThreads", wt.DWORD),
        ("th32ParentProcessID", wt.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wt.DWORD),
        ("szExeFile", wt.WCHAR * 260),
    ]


class MODULEENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wt.DWORD),
        ("th32ModuleID", wt.DWORD),
        ("th32ProcessID", wt.DWORD),
        ("GlblcntUsage", wt.DWORD),
        ("ProccntUsage", wt.DWORD),
        ("modBaseAddr", ctypes.c_void_p),
        ("modBaseSize", wt.DWORD),
        ("hModule", wt.HMODULE),
        ("szModule", wt.WCHAR * 256),
        ("szExePath", wt.WCHAR * 260),
    ]


k32.CreateToolhelp32Snapshot.argtypes = [wt.DWORD, wt.DWORD]
k32.CreateToolhelp32Snapshot.restype = wt.HANDLE
k32.Process32FirstW.argtypes = [wt.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
k32.Process32FirstW.restype = wt.BOOL
k32.Process32NextW.argtypes = [wt.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
k32.Process32NextW.restype = wt.BOOL
k32.Module32FirstW.argtypes = [wt.HANDLE, ctypes.POINTER(MODULEENTRY32W)]
k32.Module32FirstW.restype = wt.BOOL
k32.Module32NextW.argtypes = [wt.HANDLE, ctypes.POINTER(MODULEENTRY32W)]
k32.Module32NextW.restype = wt.BOOL
k32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
k32.OpenProcess.restype = wt.HANDLE
k32.CloseHandle.argtypes = [wt.HANDLE]
k32.CloseHandle.restype = wt.BOOL
k32.ReadProcessMemory.argtypes = [
    wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
]
k32.ReadProcessMemory.restype = wt.BOOL
k32.WriteProcessMemory.argtypes = [
    wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
]
k32.WriteProcessMemory.restype = wt.BOOL


def _close(handle) -> None:
    if handle and handle != INVALID_HANDLE_VALUE:
        k32.CloseHandle(handle)


def find_pids(exe_name: str) -> list[int]:
    found: list[int] = []
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == INVALID_HANDLE_VALUE:
        raise OSError(ctypes.get_last_error(), "CreateToolhelp32Snapshot(process)")
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(entry)
        ok = k32.Process32FirstW(snap, ctypes.byref(entry))
        while ok:
            if entry.szExeFile.lower() == exe_name.lower():
                found.append(int(entry.th32ProcessID))
            ok = k32.Process32NextW(snap, ctypes.byref(entry))
    finally:
        _close(snap)
    return found


def find_pid(exe_name: str) -> int:
    pids = find_pids(exe_name)
    return pids[0] if pids else 0


class MODULEINFO(ctypes.Structure):
    _fields_ = [
        ("lpBaseOfDll", ctypes.c_void_p),
        ("SizeOfImage", wt.DWORD),
        ("EntryPoint", ctypes.c_void_p),
    ]


psapi = ctypes.WinDLL("psapi", use_last_error=True)
psapi.EnumProcessModules.argtypes = [
    wt.HANDLE, ctypes.POINTER(wt.HMODULE), wt.DWORD, ctypes.POINTER(wt.DWORD),
]
psapi.EnumProcessModules.restype = wt.BOOL
psapi.GetModuleBaseNameW.argtypes = [
    wt.HANDLE, wt.HMODULE, wt.LPWSTR, wt.DWORD,
]
psapi.GetModuleBaseNameW.restype = wt.DWORD
psapi.GetModuleInformation.argtypes = [
    wt.HANDLE, wt.HMODULE, ctypes.POINTER(MODULEINFO), wt.DWORD,
]
psapi.GetModuleInformation.restype = wt.BOOL


def _module_base_psapi(pid: int, exe_name: str) -> tuple[int, int, str]:
    access = PROCESS_QUERY_INFORMATION | PROCESS_VM_READ
    h = k32.OpenProcess(access, False, pid)
    if not h:
        raise OSError(ctypes.get_last_error(), "OpenProcess (module fallback)")
    try:
        mods = (wt.HMODULE * 1024)()
        needed = wt.DWORD(0)
        if not psapi.EnumProcessModules(h, mods, ctypes.sizeof(mods), ctypes.byref(needed)):
            raise OSError(ctypes.get_last_error(), "EnumProcessModules")
        count = min(needed.value // ctypes.sizeof(wt.HMODULE), len(mods))
        for i in range(count):
            name = ctypes.create_unicode_buffer(260)
            if not psapi.GetModuleBaseNameW(h, mods[i], name, 260):
                continue
            if name.value.lower() != exe_name.lower():
                continue
            info = MODULEINFO()
            if not psapi.GetModuleInformation(h, mods[i], ctypes.byref(info),
                                              ctypes.sizeof(info)):
                raise OSError(ctypes.get_last_error(), "GetModuleInformation")
            return int(info.lpBaseOfDll or 0), int(info.SizeOfImage), name.value
    finally:
        _close(h)
    raise RuntimeError(f"{exe_name} module not found in process {pid}")


def module_base(pid: int, exe_name: str) -> tuple[int, int, str]:
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    if snap == INVALID_HANDLE_VALUE:
        # Store/packaged processes refuse module snapshots; fall back to psapi.
        return _module_base_psapi(pid, exe_name)
    try:
        entry = MODULEENTRY32W()
        entry.dwSize = ctypes.sizeof(entry)
        ok = k32.Module32FirstW(snap, ctypes.byref(entry))
        while ok:
            if entry.szModule.lower() == exe_name.lower():
                return int(entry.modBaseAddr or 0), int(entry.modBaseSize), entry.szExePath
            ok = k32.Module32NextW(snap, ctypes.byref(entry))
    finally:
        _close(snap)
    return _module_base_psapi(pid, exe_name)


class Target:
    def __init__(self, pid: int, base: int):
        self.pid = pid
        self.base = base
        access = (PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE |
                  PROCESS_QUERY_INFORMATION)
        self.handle = k32.OpenProcess(access, False, pid)
        if not self.handle:
            err = ctypes.get_last_error()
            raise OSError(err, "OpenProcess failed (try running as administrator)")

    def close(self) -> None:
        _close(self.handle)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def addr(self, rva: int) -> int:
        return self.base + rva

    def read_abs(self, addr: int, size: int) -> bytes:
        buf = ctypes.create_string_buffer(size)
        got = ctypes.c_size_t(0)
        if not k32.ReadProcessMemory(
            self.handle, ctypes.c_void_p(addr), ctypes.byref(buf),
            size, ctypes.byref(got),
        ):
            raise OSError(ctypes.get_last_error(), f"ReadProcessMemory @ {addr:#x}")
        if got.value != size:
            raise OSError(f"short read @ {addr:#x}: {got.value}/{size}")
        return buf.raw

    def u64_abs(self, addr: int) -> int:
        return struct.unpack("<Q", self.read_abs(addr, 8))[0]

    def u32_abs(self, addr: int) -> int:
        return struct.unpack("<I", self.read_abs(addr, 4))[0]

    def read(self, rva: int, size: int) -> bytes:
        return self.read_abs(self.addr(rva), size)

    def write(self, rva: int, data: bytes) -> None:
        buf = ctypes.create_string_buffer(data, len(data))
        got = ctypes.c_size_t(0)
        if not k32.WriteProcessMemory(
            self.handle, ctypes.c_void_p(self.addr(rva)), ctypes.byref(buf),
            len(data), ctypes.byref(got),
        ):
            raise OSError(ctypes.get_last_error(), f"WriteProcessMemory @ {self.addr(rva):#x}")
        if got.value != len(data):
            raise OSError(f"short write @ {self.addr(rva):#x}: {got.value}/{len(data)}")

    def u64(self, rva: int) -> int:
        return struct.unpack("<Q", self.read(rva, 8))[0]

    def u32(self, rva: int) -> int:
        return struct.unpack("<I", self.read(rva, 4))[0]

    def u8(self, rva: int) -> int:
        return self.read(rva, 1)[0]

    def put_u64(self, rva: int, value: int) -> None:
        self.write(rva, struct.pack("<Q", value))

    def put_u32(self, rva: int, value: int) -> None:
        self.write(rva, struct.pack("<I", value))

    def put_u8(self, rva: int, value: int) -> None:
        self.write(rva, struct.pack("<B", value))


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def snapshot(t: Target) -> dict:
    writer_vt = t.u64(RVA_WRITER)
    head = t.u64(RVA_LIST_HEAD)
    try:
        head_vt = t.u64(head - t.base) if head else 0
    except OSError:
        head_vt = 0
    return {
        "writer_vt": writer_vt,
        "writer_vt_ok": writer_vt == t.addr(RVA_WRITER_VTABLE),
        "writer_next": t.u64(RVA_WRITER + WRITER_NEXT),
        "writer_enabled": t.u8(RVA_WRITER + WRITER_ENABLED),
        "writer_threshold": t.u32(RVA_WRITER + WRITER_THRESHOLD),
        "writer_file": t.u64(RVA_WRITER + WRITER_FILE),
        "writer_opening": t.u8(RVA_WRITER + WRITER_OPENING),
        "head": head,
        "head_vt": head_vt,
        "linked": head == t.addr(RVA_WRITER),
        "head_is_console": head_vt == t.addr(RVA_CONSOLE_VTABLE),
        "g_debugLayers": t.u32(RVA_G_DEBUG_LAYERS),
        "logFile": t.u32(RVA_LOG_FILE),
        "logFile_SR": t.u32(RVA_LOG_FILE_SR),
    }


def print_state(t: Target, s: dict) -> None:
    print(f"  process          {t.pid}")
    print(f"  module base      {t.base:#x}")
    print(f"  writer object    {t.addr(RVA_WRITER):#x}")
    print(f"  writer vtable    {s['writer_vt']:#x} "
          f"{'OK' if s['writer_vt_ok'] else 'MISMATCH (expected %#x)' % t.addr(RVA_WRITER_VTABLE)}")
    print(f"  list head        {s['head']:#x}")
    print(f"  head vtable      {s['head_vt']:#x}")
    print(f"  writer linked    {'yes' if s['linked'] else 'no'}")
    print(f"  writer enabled   {s['writer_enabled']}")
    print(f"  writer threshold {s['writer_threshold']}")
    print(f"  writer handle    {s['writer_file']:#x}")
    print(f"  g_debugLayers    {s['g_debugLayers']}")
    print(f"  logFile          {s['logFile']}")
    print(f"  logFile_SystemRunning {s['logFile_SR']}")


def require_anchor(t: Target, s: dict) -> None:
    if not s["writer_vt_ok"]:
        raise RuntimeError(
            "writer vtable does not match idLogFileWriter. Is this the retail "
            "Epic build, and is the game fully started (past the title screen)?"
        )
    if s["head"] and not (s["head_is_console"] or s["linked"]):
        raise RuntimeError(
            f"list head {s['head']:#x} is neither the console listener nor the "
            f"writer (vtable {s['head_vt']:#x}). Refusing to write."
        )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_check(t: Target) -> int:
    s = snapshot(t)
    print("state:")
    print_state(t, s)
    if not s["writer_vt_ok"]:
        print("\nWARNING: writer vtable mismatch -- wrong build or still loading.")
    return 0


def cmd_enable(t: Target) -> int:
    s = snapshot(t)
    print("before:")
    print_state(t, s)
    require_anchor(t, s)

    if s["linked"]:
        print("\nwriter already linked; refreshing flags only.")
        old_next = s["writer_next"]
    else:
        old_next = s["head"]

    # 1. let Print pass its own gate, and flush every line
    t.put_u32(RVA_LOG_FILE, 2)
    t.put_u32(RVA_LOG_FILE_SR, 1)
    # 2. make the listener loop accept it (enabled, level >= 1)
    t.put_u8(RVA_WRITER + WRITER_ENABLED, 1)
    t.put_u32(RVA_WRITER + WRITER_THRESHOLD, 1)
    # 3. link writer -> old head, then head -> writer (order matters)
    t.put_u64(RVA_WRITER + WRITER_NEXT, old_next)
    t.put_u64(RVA_LIST_HEAD, t.addr(RVA_WRITER))
    # 4. emit layer messages at level 1
    t.put_u32(RVA_G_DEBUG_LAYERS, 1)

    s2 = snapshot(t)
    print("\nafter:")
    print_state(t, s2)
    if not s2["linked"]:
        print("\nERROR: link did not take.")
        return 1
    print("\nenabled.")
    print("  log file: <install>\\base\\qconsole.log")
    print("  the first level-1 print creates it (the writer's own 'log file ... opened'")
    print("  notice, or the next layer transition). Then walk the layer-jump volumes.")
    return 0


def cmd_undo(t: Target) -> int:
    s = snapshot(t)
    print("before:")
    print_state(t, s)
    require_anchor(t, s)

    if s["linked"]:
        if s["writer_next"]:
            t.put_u64(RVA_LIST_HEAD, s["writer_next"])
            t.put_u64(RVA_WRITER + WRITER_NEXT, 0)
        else:
            print("\nwarning: writer is the only listener; not unlinking "
                  "(that would silence the console).")
    t.put_u8(RVA_WRITER + WRITER_ENABLED, 0)
    t.put_u32(RVA_LOG_FILE, 0)
    t.put_u32(RVA_LOG_FILE_SR, 0)

    print("\nafter:")
    print_state(t, snapshot(t))
    print("\nunlinked. (qconsole.log, if any, is left in place.)")
    return 0


def cmd_off(t: Target) -> int:
    t.put_u32(RVA_G_DEBUG_LAYERS, 0)
    print(f"g_debugLayers = {t.u32(RVA_G_DEBUG_LAYERS)}")
    return 0


def _read_cstr(t: Target, addr: int, maxlen: int = 512) -> str:
    out = bytearray()
    while len(out) < maxlen:
        chunk = t.read_abs(addr + len(out), 64)
        nul = chunk.find(b"\x00")
        if nul >= 0:
            out += chunk[:nul]
            break
        out += chunk
    return out.decode("latin-1", "replace")


def cmd_dump_layers(t: Target, prefix: str) -> int:
    """List every layer name registered in the live idGameLocal."""
    game = t.u64(RVA_GAME_LOCAL)
    if not game:
        print("gameLocal is null - is a map loaded?", file=sys.stderr)
        return 1
    try:
        data = t.u64_abs(game + GL_LAYER_LIST)
        count = t.u32_abs(game + GL_LAYER_COUNT)
    except OSError as exc:
        print(f"could not read the layer registry: {exc}", file=sys.stderr)
        return 1

    print(f"gameLocal {game:#x}  list {data:#x}  entries {count}")
    if not data or count <= 0:
        print("no layers registered yet (map still loading?).", file=sys.stderr)
        return 1
    if count > 100000:
        print(f"implausible entry count {count}; refusing.", file=sys.stderr)
        return 1

    names: list[str] = []
    for i in range(count):
        try:
            p = t.u64_abs(data + i * LAYER_ENTRY_STRIDE + LAYER_ENTRY_NAME)
            if not p:
                continue
            name = _read_cstr(t, p)
        except OSError:
            continue
        if 0 < len(name) <= 200:
            names.append(name)

    if prefix:
        names = [n for n in names if prefix.lower() in n.lower()]

    for n in names:
        print(n)
    print()
    print(f"# {len(names)} name(s)")
    print("# quoted form for nextmap:")
    print('"' + " ".join(names) + '"')
    return 0


def _entity_origin(t: Target, ent: int):
    """Origin for entities whose GetOrigin is a simple lea rax,[rcx+disp]."""
    try:
        phys = t.u64_abs(ent + 0x2B8)
        if not phys:
            return None
        vt = t.u64_abs(phys)
        fn = t.u64_abs(vt + 0x90)
        code = t.read_abs(fn, 8)
        if code[0] == 0x48 and code[1] == 0x8D and code[2] == 0x41:
            off = code[3]
            return struct.unpack("<fff", t.read_abs(phys + off, 12))
        if code[:4] == b"\x31\xc0\x85\xd2":      # player: [[phys+0x58]] + 0x18
            ptr = t.u64_abs(phys + 0x58)
            if ptr:
                return struct.unpack("<fff", t.read_abs(ptr + 0x18, 12))
    except OSError:
        return None
    return None


def cmd_dump_entities(t: Target, prefix: str, positions: bool = False) -> int:
    """List the entities that exist right now (name only)."""
    game = t.u64(RVA_GAME_LOCAL)
    if not game:
        print("gameLocal is null - is a map loaded?", file=sys.stderr)
        return 1
    try:
        mgr = t.u64_abs(game + GL_ENTITY_HASH)
    except OSError as exc:
        print(f"could not read the entity manager: {exc}", file=sys.stderr)
        return 1
    if not mgr:
        print("entity manager is null (map still loading?).", file=sys.stderr)
        return 1

    base = mgr + ENTITY_ARRAY_OFF
    print(f"gameLocal {game:#x}  entity manager {mgr:#x}  array {base:#x}")

    name_re = re.compile(r"[A-Za-z0-9_./\-]{1,100}\Z")
    by_name: dict[str, int] = {}
    slots = 0
    chunk_ptrs = 0x2000          # 8192 pointers = 64 KiB per read
    for start in range(0, MAX_GENTITIES, chunk_ptrs):
        try:
            raw = t.read_abs(base + start * 8, chunk_ptrs * 8)
        except OSError:
            break
        for i in range(0, len(raw), 8):
            ent = struct.unpack_from("<Q", raw, i)[0]
            if not ent:
                continue
            slots += 1
            try:
                np = t.u64_abs(ent + ENTITY_NAME_OFF)
                if not np:
                    continue
                name = _read_cstr(t, np, 128)
            except OSError:
                continue
            if name and name_re.fullmatch(name) and name not in by_name:
                by_name[name] = ent

    names = sorted(by_name)
    if prefix:
        names = [n for n in names if prefix.lower() in n.lower()]

    for n in names:
        if positions:
            o = _entity_origin(t, by_name[n])
            if o:
                print(f"{n}  {o[0]:.1f} {o[1]:.1f} {o[2]:.1f}")
            else:
                print(f"{n}  ?")
        else:
            print(n)
    print()
    print(f"# {len(names)} entity name(s)  ({slots} occupied slots scanned)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Enable the dormant qconsole.log writer and g_debugLayers "
                    "in a running The Evil Within.",
    )
    ap.add_argument("--check", action="store_true", help="show state, change nothing")
    ap.add_argument("--undo", action="store_true", help="unlink the writer")
    ap.add_argument("--off", action="store_true", help="set g_debugLayers to 0")
    ap.add_argument("--dump-layers", action="store_true",
                    help="list every layer name registered in the live game")
    ap.add_argument("--dump-entities", action="store_true",
                    help="list the entities that currently exist")
    ap.add_argument("--positions", action="store_true",
                    help="with --dump-entities: append each entity's origin")
    ap.add_argument("--prefix", default="",
                    help="with --dump-*: only names containing this text")
    ap.add_argument("--exe", default="EvilWithin.exe", help="process name")
    ap.add_argument("--pid", type=int, default=0, help="explicit process id")
    args = ap.parse_args(argv)

    if args.pid:
        pid = args.pid
    else:
        pids = find_pids(args.exe)
        if not pids:
            print(f"{args.exe} is not running.", file=sys.stderr)
            return 2
        if len(pids) > 1:
            print(f"more than one {args.exe} is running: "
                  f"{', '.join(str(p) for p in pids)}", file=sys.stderr)
            print("re-run with --pid <id>.", file=sys.stderr)
            return 2
        pid = pids[0]

    try:
        base, size, path = module_base(pid, args.exe)
    except Exception as exc:  # noqa: BLE001
        print(f"could not read module list: {exc}", file=sys.stderr)
        print("try running this script as administrator.", file=sys.stderr)
        return 2

    print(f"{args.exe}: pid {pid}, base {base:#x}, size {size:#x}")
    print(f"  {path}")

    try:
        with Target(pid, base) as t:
            if args.check:
                return cmd_check(t)
            if args.undo:
                return cmd_undo(t)
            if args.off:
                return cmd_off(t)
            if args.dump_layers:
                return cmd_dump_layers(t, args.prefix)
            if args.dump_entities:
                return cmd_dump_entities(t, args.prefix, args.positions)
            return cmd_enable(t)
    except OSError as exc:
        print(f"win32 error: {exc}", file=sys.stderr)
        print("the game may be running elevated; try an elevated prompt.", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
