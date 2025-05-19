import math
import struct
import sys
import matplotlib.pyplot as plt
import os
import subprocess
import numpy as np

def find_and_save_lines(filename, start):
    all_results = []
    result = []
    size_line = ""
    is_saving = False

    with open(filename, 'r') as file:
        prev_line = None  # Store the previous line for pattern matching

        for line in file:
            line_strip = line.strip()
            columns = line_strip.split()

            if prev_line:
                prev_columns = prev_line.strip().split()
                
                if len(prev_columns) > 6 and len(columns) > 6 and start == 0:
                    if prev_columns[6] == "00000123" and columns[6] == "00000456":
                        if is_saving:  # If already saving, store result and reset
                            all_results.append(result)
                            result = []
                            is_saving = False
                        else:
                            is_saving = True
                if(prev_columns[6] == "feffeddc" and prev_columns[7] == "addi"):
                      start = start - 1

            if is_saving:
                if "c.mv     a1" in line_strip:
                    size_line = line_strip
                result.append(line_strip)

            prev_line = line  # Move to the next line

    if result:
        all_results.append(result)

    return all_results, size_line


def filter_lines_by_flw(lines):
    return [line for line in lines if "flw" in line]


def filter_lines_by_vle(lines):
    return [line for line in lines if "vle32.v" in line]


def extract_7th_column(lines):
    return [line.strip().split()[6] for line in lines if len(line.strip().split()) > 6]



def hex_to_float(hex_array, isVectorized=False, size=None):
    result = []
    
    for hex_str in hex_array:
        if isVectorized:
            # Split into 8-character (32-bit) chunks
            chunks = [hex_str[i:i+8] for i in range(0, len(hex_str), 8)]
            # Reverse the order (as per RISC-V vector register format)
            chunks.reverse()
        else:
            chunks = [hex_str]
        
        for chunk in chunks:
            if len(chunk) != 8:
                continue  # Skip invalid chunks
            try:
                hex_value = int(chunk, 16)
                float_value = struct.unpack('!f', struct.pack('!I', hex_value))[0]
                result.append(float_value)
            except ValueError:
                pass  # Ignore invalid hex values
    
    # Trim to the specified size if needed
    if size is not None:
        result = result[:size]
    
    return result


def print_matrixes_from_lines(lines, size):
    isVector = any("vle" in line for array in lines for line in array)

    arr = [hex_to_float(extract_7th_column(filter_lines_by_flw(matrix))) for matrix in lines]
    if (isVector):
        arr = [hex_to_float(extract_7th_column(filter_lines_by_vle(matrix)), isVectorized=isVector, size=size**2) for matrix in lines]
    print("OUSIDE:",len(arr))
    print("INSIDE: ",len(arr[0]))
    for i in range(size):
        print(arr[0][i]," ")
        #print(" ".join(f"{x:12.6f}" for x in array[i:i + size]))
    print("")
        
def print_chart_from_matrices(lines, size):
    isVector = any("vle" in line for array in lines for line in array)

    arr = [hex_to_float(extract_7th_column(filter_lines_by_flw(matrix))) for matrix in lines]
    if (isVector):
        arr = [hex_to_float(extract_7th_column(filter_lines_by_vle(matrix)), isVectorized=isVector, size=size**2) for matrix in lines]
    
    n = np.arange(size) / size

    # Plot the signal
    plt.figure(figsize=(10, 4))
    plt.plot(n, arr[0], label='Superimposed Signal', color='purple')
    plt.title('Waveform of Superimposed Signal')
    plt.xlabel('n = i / N')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
   # plt.show()
    
    #plt.savefig('superImposed.png')

def print_bar_chart_from_matrices(lines, size):
    isVector = any("vle" in line for array in lines for line in array)

    arr = [hex_to_float(extract_7th_column(filter_lines_by_flw(matrix))) for matrix in lines]
    if (isVector):
        arr = [hex_to_float(extract_7th_column(filter_lines_by_vle(matrix)), isVectorized=isVector, size=size**2) for matrix in lines]
    
        threshold = size/2 - 1

    # Step 1: Create symbol table (dictionary) of {index: value} for values >= threshold
    symbol_table = {i: val for i, val in enumerate(arr[0]) if val >= threshold}

    # Step 2: Extract keys and values for plotting
    x_labels = list(symbol_table.keys())    # Original indices (x-axis labels)
    y_values = list(symbol_table.values())  # Corresponding values (y-axis heights)

    # Step 3: Plot bar chart
    plt.figure(figsize=(10, 4))
    plt.bar(range(len(symbol_table)), y_values, color='green', width=0.3)

    # Set x-axis ticks to the original indices
    plt.xticks(ticks=range(len(symbol_table)), labels=x_labels)

    # Annotate bars with values
    for i, val in enumerate(y_values):
        plt.text(i, val + 0.01, f'{val:.2f}', ha='center', va='bottom', fontsize=9)

    plt.title('Bar Chart of FFT(input)')
    plt.xlabel('Frequencies')
    plt.ylabel('Value')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    plt.savefig('frequencies.png')
    
if __name__ == "__main__":
    size = int(sys.argv[1])
    type = sys.argv[2]
    fileName = "veer/tempFiles/logNV.txt" if type == "NV" else "veer/tempFiles/logTest.txt" if type == "Test" else "veer/tempFiles/logV.txt" 

    userInput, size_lineI = find_and_save_lines(fileName,0)
    output, size_lineO  = find_and_save_lines(fileName,1)

    if (not userInput) or (not size_lineI):
        print("Not found")
        exit()
    Inputsize = int(extract_7th_column([size_lineI])[0], 16)
    

    #print("matrix size is ", Inputsize)
    print("Type: ",type)
    print_chart_from_matrices(userInput, Inputsize)
    
    #Output
    if (not output) or (not size_lineO):
        print("Not found")
        exit()
    Outputsize = int(extract_7th_column([size_lineO])[0], 16)
    

    print("matrix size is ", Outputsize)
    
    print_bar_chart_from_matrices(output, Outputsize)