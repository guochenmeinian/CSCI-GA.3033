import subprocess
import csv
import time

# colors for printing messages in terminal
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
END_COLOR = '\033[0m'

def create_vm(zone):
    """Create a Google Compute Engine VM instance with a GPU."""
    vm_name = f'test-{zone}'
    try:
        subprocess.run([
            'gcloud', 'compute', 'instances', 'create', vm_name,
            '--zone', zone,
            '--machine-type', 'n1-standard-1',
            '--accelerator', 'type=nvidia-tesla-t4,count=1',
            '--image-family', 'debian-12',
            '--image-project', 'debian-cloud',
            '--maintenance-policy', 'TERMINATE',
            '--preemptible',
            '--quiet'
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def delete_vm(zone):
    """Delete a Google Compute Engine VM instance."""
    vm_name = f'test-{zone}'
    subprocess.run(['gcloud', 'compute', 'instances', 'delete', vm_name, '--zone', zone, '--quiet'], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

def check_gpu(zone):
    """Check if the created VM has a GPU."""
    vm_name = f'test-{zone}'
    time.sleep(30)  # wait for instance to initialize SSH
    try:
        result = subprocess.run(['gcloud', 'compute', 'ssh', vm_name, '--zone', zone, '--command', 'lspci | grep -i nvidia'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None

def main():
    output_table = "zones.csv"

    zones_output = subprocess.run(['gcloud', 'compute', 'zones', 'list', '--format', 'value(name)'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    zones_list = zones_output.stdout.splitlines()
    zone_counter = 0 # number of attempts tried

    with open(output_table, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Zone", "GPU available", "GPU allocated to VM"])

        for zone in zones_list:
            print(f"Trying to create instance in zone {zone}...")
            success, error = create_vm(zone)

            if success:
                print(f"{GREEN}Instance created in zone {zone}!{END_COLOR}")
                gpu_output = check_gpu(zone)
                if gpu_output:
                    csvwriter.writerow([zone, "yes", "yes"])
                    print(f"{YELLOW}{gpu_output}{END_COLOR}")
                else:
                    csvwriter.writerow([zone, "yes", "no"])
                    print(f"{RED}Cannot log into the instance.{END_COLOR}")
            else:
                print(f"{RED}{error}{END_COLOR}")
                csvwriter.writerow([zone, "no", "no"])
            delete_vm(zone)
            print("Instance deleted!\n")

            zone_counter += 1
            if zone_counter == 12: # exit when count reaches 12 since we only need at least 10 attempts
                break

if __name__ == "__main__":
    main()
