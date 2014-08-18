import os
import time
import opcode

def draw_frame(frame,pad=14):
    """ Return an ascii-art frame representation, suitable for stacking."""
    template = """\
| Frame {0.f_code.co_name:{fill}{align}{pad}}| -> blocks: {0.stack}
|                     | -> data: {0.block_stack}
"""
    return template.format(frame, align="<", fill=" ", pad=pad)

def draw_bytes(frame):
    """ Return the bytecode currently executing,
    with the active byte bolded."""
    bytecode = frame.f_code.co_code
    out = []

    i = 0
    while i < len(bytecode):
        if i == frame.f_lasti:
            fmt = "\x1b[31;1m{}\x1b[39;49m"
        else:
            fmt = "{}"
        byteval = ord(bytecode[i])
        out.append(fmt.format(opcode.opname[byteval]))
        if byteval >= opcode.HAVE_ARGUMENT:
            i += 3
        else:
            i += 1

    return out


def draw_vm(vm):
    divider = " --------------------- "
    out = [divider]
    for frame in reversed(vm.frames):
        out.append(draw_frame(frame))
        out.append(divider)
    out.append(divider)
    return out

def two_cols(seq1, seq2, pad=30):
    """ Return two-column view of two texts,
    given each text as a sequence"""
    template = "{0:{pad}}    {1:{pad}}"
    out = []
    for linea, lineb in zip(seq1, seq2):
        out.append(template.format(linea, lineb, pad=pad))
    return "\n".join(out)

def empty():
    while True:
        yield ""

def render_vm(vm):
    current_stack = draw_vm(vm)
    current_byte = draw_bytes(vm.frame)
    current_state = two_cols(current_stack, current_byte)
    print("\x1b[2J\x1b[H")
    print(current_state)
    time.sleep(0.2)
