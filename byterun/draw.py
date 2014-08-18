import os
import time
import opcode

EMPTY_LINE = " " * 10

def draw_frame(frame,pad=14):
    """ Return an ascii-art frame representation, suitable for stacking."""
    template = """\
| Frame {0.f_code.co_name:{fill}{align}{pad}}| -> blocks: {0.block_stack}
|                     | -> data: {0.stack}"""
    return template.format(frame, align="<", fill=" ", pad=pad)

def draw_bytes(vm):
    """ Return the bytecode currently executing,
    with the active byte bolded."""

    out = []
    for frame in vm.frames:
        if frame.f_back and frame.f_code is frame.f_back.f_code:
            continue
        out.append("Frame {}".format(frame.f_code.co_name))
        bytecode = frame.f_code.co_code
        i = 0
        while i < len(bytecode):
            if i == frame.f_lasti:
                fmt = "\x1b[31;1m{0}\x1b[39;0m"
            else:
                fmt = "\x1b[39;0m{}\x1b[39;0m"
                # fmt = "{0}"
            byteval = ord(bytecode[i])
            out.append(fmt.format(opcode.opname[byteval]))
            if byteval >= opcode.HAVE_ARGUMENT:
                i += 3
            else:
                i += 1
        out.append(EMPTY_LINE)

    return "\n".join(out)


def draw_vm(vm):
    divider = " --------------------- "
    out = [divider]
    for frame in vm.frames:
        out.append(draw_frame(frame))
        out.append(divider)
    return "\n".join(out)

def two_cols(seq1, seq2, pad=30):
    """ Return two-column view of two texts,
    given each text as a string"""
    # template = "{0:{fill}{pad}}{1:{fill}{pad}}"
    template = "{}\x1b[30G{}"
    out = []
    seq1 = seq1.split("\n")
    seq2 = seq2.split("\n")

    for linea, lineb in longzip(seq1, seq2):
        print(repr(linea), repr(lineb))
        out.append(template.format(linea.ljust(30), lineb.ljust(30)))
    return "\n".join(out)

def longzip(seq1, seq2):
    """ Zip lines together, running until both lists are exhausted"""
    padding = abs(len(seq1) - len(seq2))
    if len(seq1) > len(seq2):
        seq2 += [EMPTY_LINE] * padding
    else:
        seq1 += [EMPTY_LINE] * padding

    for pair in zip(seq1, seq2):
        yield pair


def empty():
    while True:
        yield ""

def render_vm(vm):
    current_stack = draw_vm(vm)
    current_byte = draw_bytes(vm)
    current_state = two_cols(current_byte, current_stack)
    print("\x1b[2J\x1b[H")
    print(current_state)
    time.sleep(0.3)
