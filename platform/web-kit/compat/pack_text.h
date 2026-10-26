#pragma once

#include <Python.h>
#include <cstring>

// pack.Get reads files, not network messages. The generated Python scripts
// and locale tables have an explicit contract in text_encoding.json.
inline PyObject* M2W_DecodePackText(const char* path, const void* data,
                                 Py_ssize_t size, unsigned legacyCodePage)
{
    // Every generated Python file is UTF-8. Decode it without importing any
    // Python module: textcodec imports json, whose dependencies may themselves
    // be loaded through pack.Get while textcodec is only partly initialized.
    const size_t length = std::strlen(path);
    const bool pythonSource = length >= 3 && path[length - 3] == '.' &&
        (path[length - 2] == 'p' || path[length - 2] == 'P') &&
        (path[length - 1] == 'y' || path[length - 1] == 'Y');
    if (pythonSource)
        return PyUnicode_Decode(static_cast<const char*>(data), size,
                                "utf-8-sig", "strict");

    PyObject* module = PyImport_ImportModule("textcodec");
    if (!module)
        return nullptr;
    PyObject* decode = PyObject_GetAttrString(module, "decode_pack_text");
    Py_DECREF(module);
    if (!decode)
        return nullptr;

    PyObject* bytes = PyBytes_FromStringAndSize(static_cast<const char*>(data), size);
    PyObject* source = PyUnicode_DecodeFSDefault(path);
    PyObject* codepage = PyLong_FromUnsignedLong(legacyCodePage);
    PyObject* result = nullptr;
    if (bytes && source && codepage)
        result = PyObject_CallFunctionObjArgs(decode, bytes, source, codepage, nullptr);
    Py_XDECREF(codepage);
    Py_XDECREF(source);
    Py_XDECREF(bytes);
    Py_DECREF(decode);
    return result;
}
