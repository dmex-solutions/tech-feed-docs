import subprocess
import sys
import os

def run_command(command, step_name):
    try:
        print(f"Running: {step_name} -> {command}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        print(f"Error occurred in step: {step_name}")
        print(e.stderr.decode())
        sys.exit(1)

def main():
    # Get Git branch input for merging and image tag
    # branch1 = input("Enter the branch to merge from (e.g., v25.1): ") # - uncommit this line only for UAT Build
    image_tag = input("Enter the image tag: ")

    # Define the project path
    project_path = r'D:\projects\tech-feed-docs'

    # Change to the project directory
    try:
        os.chdir(project_path)
        print(f"Changed directory to: {project_path}")
    except FileNotFoundError:
        print(f"Error: Project path {project_path} not found.")
        sys.exit(1)

    # Get the current branch # - uncommit this step only for UAT Build
    # try:
    #     current_branch = run_command('git rev-parse --abbrev-ref HEAD', "Get Current Branch").strip()
    #     print(f"Current branch is: {current_branch}")
    # except subprocess.CalledProcessError:
    #     print("Failed to determine the current branch.")
    #     sys.exit(1)

    # Step 1: Merge branch1 into the current branch # - uncommit this step only for UAT Build
    # try:
    #     run_command(f'git merge {branch1}', "Merge Branches")
    #     print(f"Successfully merged {branch1} into {current_branch}.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Merge conflict occurred while merging {branch1} into {current_branch}. Please resolve conflicts manually.")
    #     sys.exit(1)

    # Step 2: Git Pull
    run_command('git pull', "Git Pull")

    # ✅ Change directory to the actual Node project root
    os.chdir(r"technical_doc")
    print({"msg": "Changed directory to", "path": os.getcwd()})

    # Step 3: NPM Install (now executed inside technical_doc)
    run_command('npm i', "NPM Install")

    # Step 4: Docker Build
    run_command('docker image build -t qqs-tech-feed-docs -f Dockerfile .', "Docker Build")

    # Step 5: Docker Tag
    run_command(f'docker tag qqs-tech-feed-docs:latest ramalin/tech-feed-docs:{image_tag}', "Docker Tag")

    # Step 6: Docker Push
    run_command(f'docker push ramalin/tech-feed-docs:{image_tag}', "Docker Push")

if __name__ == "__main__":
    main()
