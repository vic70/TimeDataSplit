def twos_complement(input_value, num_bits):
    mask = 2 ** (num_bits - 1)
    return -(input_value & mask) + (input_value & ~mask)

def ADC_convert(input, factor = 0.3, num_bits = 16):
    mask = 2 ** (num_bits - 1)
    out = -(input & mask) + (input & ~mask) * factor /32767
    return out

def convertRes(input, Res = 0.5):
   Out = input * Res
   return Out

