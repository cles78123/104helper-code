import json
import os

# 全域路徑設定
settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.json')
saved_group_path = os.path.join(os.getcwd(), "userData", "guest", "group")

class FileUtil:
    def loadSettings(settings):
        with open(settings_path, 'r', encoding='utf-8') as file:
            return json.load(file).get(settings, {})
                
    def saveSettingsToFile(settings):
        try:
            # 打開並加載現有的 settings.json 文件
            with open(settings_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            # 遍歷 settings，找到對應的 key，並更新 status
            for key, item in settings.items():
                # 獲取當前 key 的路徑
                path = key.split('.')  # 例如 "search_company_rules.some_key"
                
                # 確定是公司規則還是職缺規則
                if 'company' in path[0]:
                    target_dict = config_data.get("search_company_rules", {})
                else:
                    target_dict = config_data.get("search_job_rules", {})

                # 確保路徑中的每一部分都存在
                for part in path[1:-1]:
                    target_dict = target_dict.get(part, {})

                # 更新該 key 下的 status
                last_part = path[-1]
                if last_part in target_dict:
                    target_dict[last_part]["status"] = item["variable"].get()

            # 將修改後的 config_data 寫回 settings.json 文件
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)

            print(f"Settings have been updated in {settings_path}")

        except FileNotFoundError:
            print(f"{settings_path} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding {settings_path}.")

    @staticmethod
    def getSavedGroups():
        """獲取所有已保存的組名稱"""
        os.makedirs(saved_group_path, exist_ok=True)
        return [f.replace('.json', '') for f in os.listdir(saved_group_path) if f.endswith('.json')]

    @staticmethod
    def loadGroupData(group_name):
        """載入指定組的數據"""
        file_path = os.path.join(saved_group_path, f"{group_name}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading group data: {str(e)}")
            return []

    @staticmethod
    def saveGroupData(group_name, data):
        """保存數據到指定組"""
        file_path = os.path.join(saved_group_path, f"{group_name}.json")
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving group data: {str(e)}")
            return False

    @staticmethod
    def deleteGroup(group_name):
        """刪除指定的組"""
        file_path = os.path.join(saved_group_path, f"{group_name}.json")
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting group: {str(e)}")
            return False