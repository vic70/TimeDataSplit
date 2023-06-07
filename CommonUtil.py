def ADC_convert(input, factor = 10, num_bits = 16):
    input_int = input.astype(int)
    mask = 2 ** (num_bits - 1)
    a = -(input_int & mask) # For debug only
    b = (input_int & ~mask) # For debug only
    out = (a + b) * factor
    return out

def convertRes(input, Res = 0.5):
   Out = input * Res
   return Out

