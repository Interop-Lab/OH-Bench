#!/usr/bin/env python3
import json
import os
import subprocess
from typing import Dict

DATASET_PATH = "dataset/main_benchmark/ohbench_arkts_v1.0.json"
TARGET_DIR = "repositories_slim"

GIT_MAPPING = {
    "applications_auth_widget": "https://gitcode.com/openharmony/applications_auth_widget.git",
    "applications_camera": "https://gitcode.com/openharmony/applications_camera.git",
    "applications_contacts": "https://gitcode.com/openharmony/applications_contacts.git",
    "applications_dlp_manager": "https://gitcode.com/openharmony/applications_dlp_manager.git",
    "applications_filepicker": "https://gitcode.com/openharmony/applications_filepicker.git",
    "applications_launcher": "https://gitcode.com/openharmony/applications_launcher.git",
    "applications_mms": "https://gitcode.com/openharmony/applications_mms.git",
    "applications_permission_manager": "https://gitcode.com/openharmony/applications_permission_manager.git",
    "applications_print_spooler": "https://gitcode.com/openharmony/applications_print_spooler.git",
    "applications_settings": "https://gitcode.com/openharmony/applications_settings.git",
    "applications_systemui": "https://gitcode.com/openharmony/applications_systemui.git",
    "applications_user_certificate_manager": "https://gitcode.com/openharmony/applications_user_certificate_manager.git",
    "codelabs": "https://gitcode.com/openharmony/codelabs.git",
    "security_privacy_center": "https://gitcode.com/openharmony/security_privacy_center.git",
    "communication_dsoftbus": "https://gitcode.com/openharmony/communication_dsoftbus.git",
    "distributedhardware_device_manager": "https://gitcode.com/openharmony/distributedhardware_device_manager.git",
    "multimedia_media_library": "https://gitcode.com/openharmony/multimedia_media_library.git",
    "ohrouter": "https://gitcode.com/openharmony-sig/ohrouter.git",
    "dialoghub": "https://gitcode.com/openharmony-sig/dialoghub.git",
    "lottie_turbo": "https://gitcode.com/openharmony-sig/lottie_turbo.git",
    "scroll_components": "https://gitcode.com/openharmony-sig/scroll_components.git",
    "ohos_ijkplayer": "https://gitcode.com/openharmony-sig/ohos_ijkplayer.git",
    "ohos_apng": "https://gitcode.com/openharmony-sig/ohos_apng.git",
    "ohos_banner": "https://gitcode.com/openharmony-sig/ohos_banner.git",
    "ohos_disklrucache": "https://gitcode.com/openharmony-sig/ohos_disklrucache.git",
    "ohos_gif-drawable": "https://gitcode.com/openharmony-sig/ohos_gif-drawable.git",
    "ohos_grpc_node": "https://gitcode.com/openharmony-sig/ohos_grpc_node.git",
    "ohos_material_progress_bar": "https://gitcode.com/openharmony-sig/ohos_material_progress_bar.git",
    "ohos_svg": "https://gitcode.com/openharmony-sig/ohos_svg.git",
    "ohos_video_trimmer": "https://gitcode.com/openharmony-sig/ohos_video_trimmer.git",
    "ohos_vlayout": "https://gitcode.com/openharmony-sig/ohos_vlayout.git",
    "ohos_wide_screen_uikit": "https://gitcode.com/openharmony-sig/ohos_wide_screen_uikit.git",
    "swipe_player": "https://gitcode.com/openharmony-sig/swipe_player.git",
    "openharmony_tpc_samples": "https://gitcode.com/openharmony-tpc/openharmony_tpc_samples.git",
    "FastBle": "https://gitcode.com/openharmony-sig/FastBle.git",
    "RocketChat": "https://gitcode.com/openharmony-tpc/RocketChat.git",
    "mixpanel-ohos": "https://gitcode.com/openharmony-tpc/mixpanel-ohos.git",
    "node_pool": "https://gitcode.com/openharmony-sig/node_pool.git",
    "ohos-beacon-library": "https://gitcode.com/openharmony-sig/ohos-beacon-library.git",
}

def load_required_commits() -> Dict[str, str]:
    """Reads the JSON dataset and extracts required project-commit mapping."""
    if not os.path.exists(DATASET_PATH):
        print(f"[Warning] Dataset JSON ({DATASET_PATH}) not found.")
        print("Fallback: Cloning repositories without checking out to specific commits.")
        return {}
        
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
        
    commit_mapping = {}
    for task in tasks:
        project = task['project']
        commit = task.get('commit_hash')
        if project and commit:
            commit_mapping[project] = commit
    return commit_mapping

def main():
    print("=" * 70)
    print("                OH-Bench Repository Recovery Engine")
    print("=" * 70)
    
    commit_mapping = load_required_commits()
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    total_repos = len(GIT_MAPPING)
    print(f"Total targets to restore: {total_repos}\n")
    
    for idx, (repo_name, git_url) in enumerate(GIT_MAPPING.items(), 1):
        repo_path = os.path.join(TARGET_DIR, repo_name)
        target_commit = commit_mapping.get(repo_name)
        
        print(f"[{idx}/{total_repos}] Restoring '{repo_name}'...")
        
        if not os.path.exists(repo_path):
            try:
                subprocess.run(
                    ["git", "clone", "--depth", "100", git_url, repo_path], 
                    check=True
                )
            except subprocess.CalledProcessError:
                print(f"  [Error] Failed to clone {repo_name} from {git_url}")
                continue
        else:
            print("  [Info] Directory already exists. Skipping clone.")

        if target_commit:
            try:
                subprocess.run(
                    ["git", "checkout", "-f", target_commit], 
                    cwd=repo_path, 
                    check=True, 
                    capture_output=True
                )
                print(f"  [Success] Checked out to commit: {target_commit}")
            except subprocess.CalledProcessError:
                print("  [Info] Commit not found in shallow history. Fetching deep commits...")
                subprocess.run(["git", "fetch", "--unshallow"], cwd=repo_path, capture_output=True)
                try:
                    subprocess.run(["git", "checkout", "-f", target_commit], cwd=repo_path, check=True)
                    print(f"  [Success] Checked out to commit: {target_commit}")
                except subprocess.CalledProcessError:
                    print(f"  [Error] Failed to checkout to commit {target_commit} for {repo_name}")
        else:
            print("  [Warning] No specific commit registered in dataset. Kept at default branch.")
            
        print("-" * 70)

    print("\n[Complete] Benchmark repositories restoration finished successfully.")
    print(f"Location: {os.path.abspath(TARGET_DIR)}")

if __name__ == "__main__":
    main()
