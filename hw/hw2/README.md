# gcloud GPU chase

• Situation: You are working for a small company, you don’t get GCP premium support, your company needs 1 GPU to run an urgent AI model

• Mission: Find a zone and a GPU type that your company can use (any GPU is fine)

• Submission:
- Code that iterates through all regions and zones of google cloud and attempts to create a VM with the selected GPU type
- Output:
    - VM creation successful, or failed with a given reason (no resource type, no capacity)
    - A table with at least 10 zones tested, GPU available (yes/no), GPU allocated to VM (yes/no)

Code is implemented with and python and gcloud shell command scripts

### Usage
simply run hw2.py in gcloud terminal as followed:
> python hw2.py