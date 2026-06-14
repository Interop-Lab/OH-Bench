import json

FILE_A = "data/arkts_dataset_final.json"
FILE_B = "data/cpp_dataset_final.json"
OUTPUT = "data/oh_bench_complete.json"

def main():
    data = []
    if os.path.exists(FILE_A):
        with open(FILE_A) as f:
            data.extend(json.load(f))
            
    if os.path.exists(FILE_B):
        with open(FILE_B) as f:
            data.extend(json.load(f))
            
    with open(OUTPUT, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"合并完成！总共 {len(data)} 个任务。")
    print(f"ArkTS + Cpp -> {OUTPUT}")

if __name__ == "__main__":
    import os
    main()