def twos_complement(input_value, num_bits):
    mask = 2 ** (num_bits - 1)
    return -(input_value & mask) + (input_value & ~mask)

def ADC_convert(input, factor = 0.3, num_bits = 8):
    input_int = int(input)
    mask = 2 ** (num_bits - 1)
    out = -(input_int & mask) + (input_int & ~mask) * factor /32767
    return out

def convertRes(input, Res = 0.5):
   Out = input * Res
   return Out

