#include "pack_text.h"
#include <cstdio>

// Exercises the exact C++ -> Python boundary used by pack.Get. Linked to a
// host CPython for fast regression testing; the wasm build is a separate gate.
static bool Check(const char* path, const char* bytes, Py_ssize_t size,
                  unsigned page, const char* expected)
{
    PyObject* value = M2W_DecodePackText(path, bytes, size, page);
    if (!value)
    {
        PyErr_Print();
        return false;
    }
    const char* actual = PyUnicode_AsUTF8(value);
    const bool ok = actual && std::strcmp(actual, expected) == 0;
    Py_DECREF(value);
    return ok;
}

int main(int argc, char** argv)
{
    if (argc != 2)
        return 2;
    Py_Initialize();
    PyObject* directory = PyUnicode_DecodeFSDefault(argv[1]);
    if (!directory || PyList_Insert(PySys_GetObject("path"), 0, directory) < 0)
        return 3;
    Py_DECREF(directory);

    // Simulate the game's custom pack importer, including a module without
    // __file__. Importing the codec must not re-enter its own decoder.
    const char* setup =
        "import builtins, os, sys, types\n"
        "os.chdir(sys.path[0])\n"
        "old_import = builtins.__import__\n"
        "import _pack_text_test\n"
        "def packed_import(name, *args, **kwargs):\n"
        "    if name == 'json':\n"
        "        assert _pack_text_test.decode('codec_dependency.PY', b'# dependency', 1254) == '# dependency'\n"
        "    if name == 'textcodec' and name not in sys.modules:\n"
        "        module = types.ModuleType(name)\n"
        "        sys.modules[name] = module\n"
        "        with open('textcodec.py', 'rb') as source:\n"
        "            text = _pack_text_test.decode('textcodec.py', source.read(), 1254)\n"
        "        exec(compile(text, 'textcodec.py', 'exec'), module.__dict__)\n"
        "        return module\n"
        "    return old_import(name, *args, **kwargs)\n"
        "builtins.__import__ = packed_import\n";
    // First test the bootstrap decoder itself before importing textcodec.
    bool ok = Check("textcodec.py", "# UTF-8\n", 8, 1254, "# UTF-8\n");

    // The real import path is tested by installing a tiny native module.
    static PyMethodDef methods[] = {
        {"decode", [](PyObject*, PyObject* args) -> PyObject* {
             const char* path = nullptr;
             const char* bytes = nullptr;
             Py_ssize_t size = 0;
             unsigned page = 0;
             if (!PyArg_ParseTuple(args, "sy#I", &path, &bytes, &size, &page))
                 return nullptr;
             return M2W_DecodePackText(path, bytes, size, page);
         }, METH_VARARGS, nullptr},
        {nullptr, nullptr, 0, nullptr}
    };
    static PyModuleDef definition = {
        PyModuleDef_HEAD_INIT, "_pack_text_test", nullptr, -1, methods
    };
    PyObject* module = PyModule_Create(&definition);
    if (!module || PyDict_SetItemString(PyImport_GetModuleDict(), "_pack_text_test", module) < 0)
        return 4;
    Py_DECREF(module);
    if (PyRun_SimpleString(setup) != 0)
        return 5;

    const char* title = "Sava\xc5\x9f Bileti Se\xc3\xa7iniz";
    ok = Check("uiMiniMap.py", title, std::strlen(title), 1254, title) && ok;
    const char* free = "\xdc" "cretsiz";
    ok = Check("locale/tr/locale_interface.txt", free, 8, 1252,
               "\xc3\x9c" "cretsiz") && ok;
    const char* polish = "\xc5\x81\xc3\xb3" "d\xc5\xba";
    ok = Check("locale/pl/locale_game.txt", polish, std::strlen(polish), 1254, polish) && ok;
    // Once the contract module has loaded, the native script fast path must
    // still agree with its declared source encoding.
    ok = PyRun_SimpleString(
        "import textcodec\n"
        "assert textcodec.CONTRACT['generated_python'] == 'utf-8-sig'\n") == 0 && ok;
    PyObject* invalid = M2W_DecodePackText("uiBad.py", "\xff", 1, 1254);
    ok = !invalid && PyErr_Occurred() && ok;
    Py_XDECREF(invalid);
    PyErr_Clear();
    Py_Finalize();
    std::puts(ok ? "pack text boundary: PASS" : "pack text boundary: FAIL");
    return ok ? 0 : 1;
}
