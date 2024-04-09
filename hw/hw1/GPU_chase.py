import subprocess
import json

def get_regions():
    regions_command = "gcloud compute regions list --format=json"
    regions_output = subprocess.run(regions_command, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    regions = json.loads(regions_output.stdout)
    return [region['name'] for region in regions]

def get_zones_in_region(region):
    zones_command = f"gcloud compute zones list --filter=region={region} --format=json"
    zones_output = subprocess.run(zones_command, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    zones = json.loads(zones_output.stdout)
    return [zone['name'] for zone in zones]

def create_vm_with_gpu(zone):
    vm_name = "gpu-vm-test"
    machine_type = "n1-standard-1"
    gpu_type = "nvidia-tesla-t4"
    gpu_count = 1
    create_vm_command = f"gcloud compute instances create {vm_name} --zone={zone} --machine-type={machine_type} --accelerator=\"type={gpu_type},count={gpu_count}\" --maintenance-policy=TERMINATE --restart-on-failure --format=json"
    try:
        subprocess.run(create_vm_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return "Yes"
    except subprocess.CalledProcessError as e:
        return "No, " + e.stderr.split('\n')[-2]

def main():
    results = []
    regions = get_regions()
    for region in regions:
        zones = get_zones_in_region(region)
        for zone in zones:
            gpu_allocation_result = create_vm_with_gpu(zone)
            results.append((zone, "Yes", gpu_allocation_result))
            if len(results) >= 10:  # Limit to first 10 zones for brevity
                break
        if len(results) >= 10:
            break
            
    print("Zone", "GPU Available", "GPU Allocated to VM")
    for result in results:
        print(result[0], result[1], result[2])

if __name__ == "__main__":
    main()
