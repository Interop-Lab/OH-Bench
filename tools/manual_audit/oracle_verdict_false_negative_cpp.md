# Oracle Verdict Audit - False Negatives (C/C++)

## [1/50] ID: CPP_0358 | C/C++ (F)
- **Rule ID:** `cppcheck/memleak`
- **Result:** `SECONDARY_DEFECT: 39`
- **Target File:** `ijkplayer/src/main/cpp/napi/ijkplayer_napi.cpp`
- **Warning:** Memory leak: context

### Buggy Snippet
```cpp
void messageCallBack(int what, int arg1, int arg2, char *obj, std::string id)
{
    LOGI("napi-->messageCallBack");
    struct CallbackContext *context = new CallbackContext();
    IJKPlayerNapi *instance = IJKPlayerNapi::getInstance(id);
    context->env = instance->envMessage_;
    uv_loop_s *loopMessage = nullptr;
    napi_get_uv_event_loop(context->env, &loopMessage);
    if (loopMessage == nullptr) {
        LOGI("napi-->loopMessage null");
        return;
    }
    uv_work_t *work = new (std::nothrow) uv_work_t;
    if (work == nullptr) {
        LOGI("napi-->work null");
        return;
    }
    context->what = what;
    context->arg1 = arg1;
    context->arg2 = arg2;
    context->obj = obj;
    context->callbackRef = instance->callBackRefMessage_;
    work->data = (void *)context;
    uv_queue_work(
        loopMessage, work, [](uv_work_t *work) {},
        [](uv_work_t *work, int status) {
            LOGI("napi-->uv_queue_work");
            CallbackContext *context = static_cast<CallbackContext *>(work->data);
            napi_value callback = nullptr;
            napi_get_reference_value(context->env, context->callbackRef, &callback);
            napi_value what_;
            napi_value arg1_;
            napi_value arg2_;
            napi_value obj_;
            napi_create_int32(context->env, context->what, &what_);
            napi_create_int32(context->env, context->arg1, &arg1_);
            napi_create_int32(context->env, context->arg2, &arg2_);
            napi_value ret = 0;
            if (context->obj) {
                napi_create_string_utf8(context->env, context->obj, NAPI_AUTO_LENGTH, &obj_);
                napi_value argv_4[] = {what_, arg1_, arg2_, obj_};
                napi_call_function(context->env, nullptr, callback, PARAM_COUNT_4, argv_4, &ret);
            } else {
                napi_value argv_3[] = {what_, arg1_, arg2_};
                napi_call_function(context->env, nullptr, callback, PARAM_COUNT_3, argv_3, &ret);
            }
            if (work != nullptr) {
                delete work;
            }
            delete context;
            LOGI("napi-->uv_queue_work end");
        });
}
```

### Patch
```diff
// File: ijkplayer/src/main/cpp/napi/ijkplayer_napi.cpp
--- a/ijkplayer/src/main/cpp/napi/ijkplayer_napi.cpp
+++ b/ijkplayer/src/main/cpp/napi/ijkplayer_napi.cpp
@@ -78,11 +78,13 @@
     napi_get_uv_event_loop(context->env, &loopMessage);
     if (loopMessage == nullptr) {
         LOGI("napi-->loopMessage null");
+        delete context;
         return;
     }
     uv_work_t *work = new (std::nothrow) uv_work_t;
     if (work == nullptr) {
         LOGI("napi-->work null");
+        delete context;
         return;
     }
     context->what = what;


```

---

## [2/50] ID: CPP_0084 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'strTableName' should be passed by const reference.

### Buggy Snippet
```cpp
int64_t T2lGetTableLong(string strTableName, string strVarLong)
{
    auto L = g_L; /* variable in Lua */
    lua_getglobal(L, strTableName.c_str());
    if (!lua_istable(L, -1)) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0, "ohos_luaarkts", "T2lGetTableLong: %{public}s is not a table",
                     strTableName.c_str());
        return 0;
    }
    lua_getfield(L, -1, strVarLong.c_str());
    int64_t valLong = lua_tonumber(L, -1);

    return valLong;
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -227,7 +227,7 @@
 }
 
 
-int T2lGetTableInt(string strTableName, string strVarInt)
+int T2lGetTableInt(const string& strTableName, const string& strVarInt)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, strTableName.c_str());
@@ -242,7 +242,7 @@
     return valInt;
 }
 
-int64_t T2lGetTableLong(string strTableName, string strVarLong)
+int64_t T2lGetTableLong(const string& strTableName, const string& strVarLong)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, strTableName.c_str());
@@ -257,7 +257,7 @@
     return valLong;
 }
 
-double T2lGetTableDouble(string strTableName, string strVarDouble)
+double T2lGetTableDouble(const string& strTableName, const string& strVarDouble)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, strTableName.c_str());
@@ -272,7 +272,7 @@
     return valDouble;
 }
 
-const char *T2lGetTableChar(string strTableName, string strVarChar)
+const char *T2lGetTableChar(const string& strTableName, const string& strVarChar)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, strTableName.c_str());
@@ -288,7 +288,7 @@
     return valChar;
 }
 
-int T2lGetTableBool(string strTableName, string strVarBool)
+int T2lGetTableBool(const string& strTableName, const string& strVarBool)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, strTableName.c_str());


```

---

## [3/50] ID: CPP_0020 | C/C++ (F)
- **Rule ID:** `cppcheck/knownConditionTrueFalse`
- **Result:** `LINTER_FAIL`
- **Target File:** `napi/settings/napi_settings.cpp`
- **Warning:** Condition 'asyncCallbackInfo!=nullptr' is always true

### Buggy Snippet
```cpp
/**
 * @brief setValue NAPI implementation.
 *
 * @param env the environment that the Node-API call is invoked under
 * @param info the callback info passed into the callback function
 * @return napi_value the return value from NAPI C++ to JS for the module.
 */
napi_value napi_set_value(napi_env env, napi_callback_info info)
{
    SETTING_LOG_INFO("n_s_v");

    // getValue api need 3 parameters when Promise mode and need 4 parameters when callback mode
    const size_t paramOfCallback = ARGS_FOUR;

    size_t argc = ARGS_FIVE;
    napi_value args[ARGS_FIVE] = {nullptr};
    NAPI_CALL(env, napi_get_cb_info(env, info, &argc, args, nullptr, nullptr));
    if (argc != ARGS_THREE && argc != ARGS_FOUR && argc != ARGS_FIVE) {
        SETTING_LOG_ERROR(
            "set %{public}s, wrong number of arguments, expect 3 or 4 or 5 but get %{public}zd",
            __func__,
            argc);
        return wrap_void_to_js(env);
    }

    SETTING_LOG_INFO("set  aft create aysnc call back info");
    napi_valuetype valueType;
    NAPI_CALL(env, napi_typeof(env, args[PARAM0], &valueType));
    NAPI_ASSERT(env, valueType == napi_object, "Wrong argument[0] type. Object expected.");
    NAPI_CALL(env, napi_typeof(env, args[PARAM1], &valueType));
    NAPI_ASSERT(env, valueType == napi_string, "Wrong argument[1], type. String expected");
    NAPI_CALL(env, napi_typeof(env, args[PARAM2], &valueType));
    NAPI_ASSERT(env, valueType == napi_string, "Wrong argument[2], type. String expected");

    // api9 napi_set_value_ext
    bool stageMode = false;
    napi_status status = OHOS::AbilityRuntime::IsStageContext(env, args[PARAM0], stageMode);
    if (status == napi_ok) {
        SETTING_LOG_INFO("argv[0] is a context, Stage Model: %{public}d", stageMode);
        return napi_set_value_ext(env, info, stageMode);
    }

    NAPIDataAbilityHelperWrapper* wrapper = nullptr;
    NAPI_CALL(env, napi_unwrap(env, args[PARAM0], reinterpret_cast<void **>(&wrapper)));

    SETTING_LOG_INFO("set  arg count is %{public}zd", argc);
    // Check the value type of the arguments
    AsyncCallbackInfo* asyncCallbackInfo = new AsyncCallbackInfo {
        .env = env,
        .asyncWork = nullptr,
        .deferred = nullptr,
        .callbackRef = nullptr,
        .dataAbilityHelper = nullptr,
        .key = "",
        .value = "",
        .uri = "",
        .status = false,
    };
    if (asyncCallbackInfo == nullptr) {
        SETTING_LOG_ERROR("asyncCallbackInfo is null");
        return wrap_void_to_js(env);
    }
    if (wrapper != nullptr) {
        asyncCallbackInfo->dataAbilityHelper = wrapper->GetDataAbilityHelper();
    }
	
    asyncCallbackInfo->key = unwrap_string_from_js(env, args[PARAM1]);
    asyncCallbackInfo->value = unwrap_string_from_js(env, args[PARAM2]);
    SETTING_LOG_INFO("set  input param is : (key %{public}s, value %{public}s)",
        asyncCallbackInfo->key.c_str(), asyncCallbackInfo->value.c_str());

    napi_value ret = nullptr;
    if (argc == paramOfCallback) {
        napi_create_reference(env, args[PARAM3], 1, &asyncCallbackInfo->callbackRef);
        ret = SetValueAsync(env, asyncCallbackInfo);
    } else {
        ret = SetValuePromise(env, asyncCallbackInfo);
    }
    if (asyncCallbackInfo != nullptr) {
        asyncCallbackInfo = nullptr;
    }
    SETTING_LOG_INFO("set  value end");
    return ret;
}
```

### Patch
```diff
// File: napi/settings/napi_settings.cpp
--- a/napi/settings/napi_settings.cpp
+++ b/napi/settings/napi_settings.cpp
@@ -275,7 +275,7 @@
     }
 
     SETTING_LOG_INFO("uri arg count is %{public}zd", argc);
-    AsyncCallbackInfo* asyncCallbackInfo = new AsyncCallbackInfo {
+    AsyncCallbackInfo* asyncCallbackInfo = new (std::nothrow) AsyncCallbackInfo {
         .env = env,
         .asyncWork = nullptr,
         .deferred = nullptr,
@@ -1410,7 +1410,7 @@
     if (wrapper != nullptr) {
         asyncCallbackInfo->dataAbilityHelper = wrapper->GetDataAbilityHelper();
     }
-	
+        
     asyncCallbackInfo->key = unwrap_string_from_js(env, args[PARAM1]);
     asyncCallbackInfo->value = unwrap_string_from_js(env, args[PARAM2]);
     SETTING_LOG_INFO("set  input param is : (key %{public}s, value %{public}s)",


```

---

## [4/50] ID: CPP_0014 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `cj/settings/src/cj_settings.cpp`
- **Warning:** Function parameter 'str' should be passed by const reference.

### Buggy Snippet
```cpp
/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "cj_settings.h"
#include <cstdint>
#include <vector>
#include "cj_common_ffi.h"
#include "cj_settings_log.h"
#include "cj_settings_utils.h"
#include "os_account_manager.h"
#include "securec.h"
#include "uri.h"

namespace OHOS {
namespace CJSystemapi {
namespace CJSettings {
const std::string SETTINGS_DATA_BASE_URI = "dataability:///com.ohos.settingsdata.DataAbility";
const std::string SETTINGS_DATA_FIELD_KEYWORD = "KEYWORD";
const std::string SETTINGS_DATA_FIELD_VALUE = "VALUE";
const int32_t PERMISSION_EXCEPTION_CODE = 201;
const int32_t PERMISSION_DENIED_CODE = -2;
const int32_t USERID_HELPER_NUMBER = 100;
const int32_t PARAM_ERROR = 401;
const int32_t MEMORY_CODE = 14700104;

char* TransformFromString(std::string str, int32_t* ret)
{
    uint64_t len = str.size() + 1;
    char* retValue = static_cast<char *>(malloc(len));
    if (retValue == nullptr) {
        *ret = MEMORY_CODE;
        return nullptr;
    }
    *ret = memcpy_s(retValue, len, str.c_str(), len);
    if (*ret != 0) {
        *ret = MEMORY_CODE;
    }
    return retValue;
}
```

### Patch
```diff
// File: cj/settings/src/cj_settings.cpp
--- a/cj/settings/src/cj_settings.cpp
+++ b/cj/settings/src/cj_settings.cpp
@@ -35,7 +35,7 @@
 const int32_t PARAM_ERROR = 401;
 const int32_t MEMORY_CODE = 14700104;
 
-char* TransformFromString(std::string str, int32_t* ret)
+char* TransformFromString(const std::string& str, int32_t* ret)
 {
     uint64_t len = str.size() + 1;
     char* retValue = static_cast<char *>(malloc(len));


```

---

## [5/50] ID: CPP_0172 | C/C++ (F)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `SECONDARY_DEFECT: 23`
- **Target File:** `vap/vap_module/src/main/cpp/render/plugin_render.cpp`
- **Warning:** Consider using std::find_if algorithm instead of a raw loop.

### Buggy Snippet
```cpp
static void FoundSrcInfo(napi_env env, const std::string& srcId, AnimConfig& animConfig, NVal& srcInfo)
{
    if (animConfig.frameAllPtr == nullptr || animConfig.frameAllPtr->frameAll.empty()) {
        return;
    }

    for (const auto& frame : animConfig.frameAllPtr->frameAll) {
        bool found = false;
        for (const auto& src : frame.second.frames) {
            if (src.srcId == srcId) {
                auto x = NVal::CreateInt64(env, static_cast<int>(src.frame.x));
                auto y = NVal::CreateInt64(env, static_cast<int>(src.frame.y));
                srcInfo.AddProp("x", x.val_);
                srcInfo.AddProp("y", y.val_);
                found = true;
                break;
            }
        }
        if (found) {
            break;
        }
    }
}
```

### Patch
```diff
// File: vap/vap_module/src/main/cpp/render/plugin_render.cpp
--- a/vap/vap_module/src/main/cpp/render/plugin_render.cpp
+++ b/vap/vap_module/src/main/cpp/render/plugin_render.cpp
@@ -17,6 +17,7 @@
 
 #include <multimedia/image_framework/image/image_source_native.h>
 #include <multimedia/image_framework/image_pixel_map_mdk.h>
+#include <algorithm>
 #include <cstdint>
 #include <string>
 #include <js_native_api.h>
@@ -335,18 +336,13 @@
     }
 
     for (const auto& frame : animConfig.frameAllPtr->frameAll) {
-        bool found = false;
-        for (const auto& src : frame.second.frames) {
-            if (src.srcId == srcId) {
-                auto x = NVal::CreateInt64(env, static_cast<int>(src.frame.x));
-                auto y = NVal::CreateInt64(env, static_cast<int>(src.frame.y));
-                srcInfo.AddProp("x", x.val_);
-                srcInfo.AddProp("y", y.val_);
-                found = true;
-                break;
-            }
-        }
-        if (found) {
+        auto it = std::find_if(frame.second.frames.begin(), frame.second.frames.end(),
+                               [&srcId](const auto& src) { return src.srcId == srcId; });
+        if (it != frame.second.frames.end()) {
+            auto x = NVal::CreateInt64(env, static_cast<int>(it->frame.x));
+            auto y = NVal::CreateInt64(env, static_cast<int>(it->frame.y));
+            srcInfo.AddProp("x", x.val_);
+            srcInfo.AddProp("y", y.val_);
             break;
         }
     }


```

---

## [6/50] ID: CPP_0027 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `napi/settings/napi_settings.cpp`
- **Warning:** Function parameter 'tableName' should be passed by const reference.

### Buggy Snippet
```cpp
std::shared_ptr<DataShareHelper> getDataShareHelper(napi_env env, sptr<IRemoteObject> token, std::string tableName,
                                                    AsyncCallbackInfo *asyncCallbackInfo)
{
    if (globalDataShareHelper != nullptr) {
        SETTING_LOG_INFO("u_c");
        return globalDataShareHelper;
    }
    std::lock_guard<std::mutex> lockGuard(helper);
    if (globalDataShareHelper != nullptr) {
        SETTING_LOG_INFO("l_u_c");
        return globalDataShareHelper;
    }
    std::shared_ptr<OHOS::DataShare::DataShareHelper> dataShareHelper = nullptr;
    std::string strProxyUri = GetProxyUriStr(tableName, USERID_HELPER_NUMBER);
    OHOS::Uri proxyUri(strProxyUri);
    dataShareHelper = OHOS::DataShare::DataShareHelper::Creator(token, strProxyUri, "");
    if (!dataShareHelper) {
        SETTING_LOG_ERROR("dataShareHelper from proxy is null");
        dataShareHelper = getNoSilentDataShareHelper(env, asyncCallbackInfo);
    } else {
        SETTING_LOG_INFO("create global helper");
        globalDataShareHelper = dataShareHelper;
        std::string strUri = "datashare:///com.ohos.settingsdata.DataAbility";
        dataShareHelper->SetDataShareHelperExtUri(strUri);
    }
    return dataShareHelper;
}
```

### Patch
```diff
// File: napi/settings/napi_settings.cpp
--- a/napi/settings/napi_settings.cpp
+++ b/napi/settings/napi_settings.cpp
@@ -420,7 +420,7 @@
     return dataShareHelper;
 }
 
-std::shared_ptr<DataShareHelper> getDataShareHelper(napi_env env, sptr<IRemoteObject> token, std::string tableName,
+std::shared_ptr<DataShareHelper> getDataShareHelper(napi_env env, sptr<IRemoteObject> token, const std::string& tableName,
                                                     AsyncCallbackInfo *asyncCallbackInfo)
 {
     if (globalDataShareHelper != nullptr) {
@@ -1410,7 +1410,7 @@
     if (wrapper != nullptr) {
         asyncCallbackInfo->dataAbilityHelper = wrapper->GetDataAbilityHelper();
     }
-	
+        
     asyncCallbackInfo->key = unwrap_string_from_js(env, args[PARAM1]);
     asyncCallbackInfo->value = unwrap_string_from_js(env, args[PARAM2]);
     SETTING_LOG_INFO("set  input param is : (key %{public}s, value %{public}s)",
@@ -1860,7 +1860,7 @@
 }
 
 // get uri for stage model
-std::string GetStageUriStr(std::string tableName, int id, std::string keyStr)
+std::string GetStageUriStr(const std::string& tableName, int id, const std::string& keyStr)
 {
     if (id < USERID_HELPER_NUMBER) {
         id = USERID_HELPER_NUMBER;
@@ -1887,7 +1887,7 @@
 }
 
 // get proxy uri
-std::string GetProxyUriStr(std::string tableName, int id)
+std::string GetProxyUriStr(const std::string& tableName, int id)
 {
     if (id < USERID_HELPER_NUMBER) {
         id = USERID_HELPER_NUMBER;
@@ -1909,7 +1909,7 @@
 }
 
 // check whether tableName is invalid, invalid -> true valid -> false
-bool IsTableNameInvalid(std::string tableName)
+bool IsTableNameInvalid(const std::string& tableName)
 {
     if (tableName != "global" && tableName != "system" && tableName != "secure") {
         return true;


```

---

## [7/50] ID: CPP_0109 | C/C++ (F)
- **Rule ID:** `cppcheck/knownConditionTrueFalse`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_smack/library/src/main/cpp/room.cpp`
- **Warning:** Condition 'data==nullptr' is always false

### Buggy Snippet
```cpp
void room::handleMUCConfigForm(MUCRoom *room, const DataForm &form)
{
    if (room == nullptr) {
        LOGE("SMACK_TAG---------> [room.handleMUCConfigForm]room is null");
        return;
    }
    // todo 房间配置信息处理处
    LOGD("requestRoomConfig handleMUCConfigForm room:%s, title:%s, form:%s", room->name().c_str(),
         form.title().c_str(), form.filterString().c_str());
    LOGD("requestRoomConfig handleMUCConfigForm tag:%s", form.tag()->xml().c_str());

    ThreadSafeRoomInfo *data = &g_threadRoomInfo;
    if (data == nullptr) {
        LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
        return;
    }
    data->roomInfo = form.tag()->xml().c_str();
    NapiJsCallBack(data);
}
```

### Patch
```diff
// File: ohos_smack/library/src/main/cpp/room.cpp
--- a/ohos_smack/library/src/main/cpp/room.cpp
+++ b/ohos_smack/library/src/main/cpp/room.cpp
@@ -856,10 +856,6 @@
     jsonStr.append("}");
     LOGD("handleMUCParticipantPresence ===>>>> %s %s \n", nick.c_str(), flagType.c_str());
     ThreadSafeInfoMUCP *data = &g_threadInfoMUCP;
-    if (data == nullptr) {
-        LOGE("SMACK_TAG---------> [room.handleMUCParticipantPresence]data is null");
-        return;
-    }
     data->nike = nick.c_str();
     data->presenceType = jsonStr.c_str();
     napi_acquire_threadsafe_function(tsfn_mucp);
@@ -885,10 +881,6 @@
     LOGI("smack handleMUCMessage  %s:  %d", "handleMUCMessage work  ", __LINE__);
 
     ThreadSafeInfoRoom *data = &g_threadInfoRoom;
-	if (data == nullptr) {
-        LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
-        return;
-    }
     data->id = msg.from().resource().c_str();
     data->msg = body.c_str();
     LOGI("SMACK_TAG--------->: %s:  %d", "handleMUCMessage: ", __LINE__);
@@ -924,10 +916,6 @@
         features, name.c_str(), infoForm->tag()->xml().c_str());
 
     ThreadSafeRoomInfo *data = &g_threadRoomInfo;
-    if (data == nullptr) {
-        LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
-        return;
-    }
     data->roomInfo = infoForm->tag()->xml().c_str();
     NapiJsCallBack(data);
 }
@@ -961,10 +949,6 @@
     LOGD("requestRoomConfig handleMUCConfigForm tag:%s", form.tag()->xml().c_str());
 
     ThreadSafeRoomInfo *data = &g_threadRoomInfo;
-    if (data == nullptr) {
-        LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
-        return;
-    }
     data->roomInfo = form.tag()->xml().c_str();
     NapiJsCallBack(data);
 }
@@ -1026,7 +1010,7 @@
 
 void room::handleMUCConfigList(MUCRoom *room, const MUCListItemList &items, MUCOperation operation)
 {
-	if (room == nullptr) {
+        if (room == nullptr) {
         LOGE("SMACK_TAG---------> [room.handleMUCConfigList]room is null");
         return;
     }


```

---

## [8/50] ID: CPP_0156 | C/C++ (F)
- **Rule ID:** `cppcheck/variableScope`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `spinec/Spinec/src/main/cpp/thirdparty/spinec/spine/SkeletonClipping.c`
- **Warning:** The scope of the variable 'p1x' can be reduced.

### Buggy Snippet
```cpp
static void _makeClockwise(spFloatArray *polygon) {
	int i, n, lastX;
	float *vertices = polygon->items;
	int verticeslength = polygon->size;

	float area =
				  vertices[verticeslength - 2] * vertices[1] - vertices[0] * vertices[verticeslength - 1],
		  p1x, p1y, p2x, p2y;
	for (i = 0, n = verticeslength - 3; i < n; i += 2) {
		p1x = vertices[i];
		p1y = vertices[i + 1];
		p2x = vertices[i + 2];
		p2y = vertices[i + 3];
		area += p1x * p2y - p2x * p1y;
	}
	if (area < 0) return;

	for (i = 0, lastX = verticeslength - 2, n = verticeslength >> 1; i < n; i += 2) {
		float x = vertices[i], y = vertices[i + 1];
		int other = lastX - i;
		vertices[i] = vertices[other];
		vertices[i + 1] = vertices[other + 1];
		vertices[other] = x;
		vertices[other + 1] = y;
	}
}
```

### Patch
```diff
// File: spinec/Spinec/src/main/cpp/thirdparty/spinec/spine/SkeletonClipping.c
--- a/spinec/Spinec/src/main/cpp/thirdparty/spinec/spine/SkeletonClipping.c
+++ b/spinec/Spinec/src/main/cpp/thirdparty/spinec/spine/SkeletonClipping.c
@@ -31,307 +31,306 @@
 #include <spine/extension.h>
 
 spSkeletonClipping *spSkeletonClipping_create(void) {
-	spSkeletonClipping *clipping = CALLOC(spSkeletonClipping, 1);
-
-	clipping->triangulator = spTriangulator_create();
-	clipping->clippingPolygon = spFloatArray_create(128);
-	clipping->clipOutput = spFloatArray_create(128);
-	clipping->clippedVertices = spFloatArray_create(128);
-	clipping->clippedUVs = spFloatArray_create(128);
-	clipping->clippedTriangles = spUnsignedShortArray_create(128);
-	clipping->scratch = spFloatArray_create(128);
-
-	return clipping;
+        spSkeletonClipping *clipping = CALLOC(spSkeletonClipping, 1);
+
+        clipping->triangulator = spTriangulator_create();
+        clipping->clippingPolygon = spFloatArray_create(128);
+        clipping->clipOutput = spFloatArray_create(128);
+        clipping->clippedVertices = spFloatArray_create(128);
+        clipping->clippedUVs = spFloatArray_create(128);
+        clipping->clippedTriangles = spUnsignedShortArray_create(128);
+        clipping->scratch = spFloatArray_create(128);
+
+        return clipping;
 }
 
 void spSkeletonClipping_dispose(spSkeletonClipping *self) {
-	spTriangulator_dispose(self->triangulator);
-	spFloatArray_dispose(self->clippingPolygon);
-	spFloatArray_dispose(self->clipOutput);
-	spFloatArray_dispose(self->clippedVertices);
-	spFloatArray_dispose(self->clippedUVs);
-	spUnsignedShortArray_dispose(self->clippedTriangles);
-	spFloatArray_dispose(self->scratch);
-	FREE(self);
+        spTriangulator_dispose(self->triangulator);
+        spFloatArray_dispose(self->clippingPolygon);
+        spFloatArray_dispose(self->clipOutput);
+        spFloatArray_dispose(self->clippedVertices);
+        spFloatArray_dispose(self->clippedUVs);
+        spUnsignedShortArray_dispose(self->clippedTriangles);
+        spFloatArray_dispose(self->scratch);
+        FREE(self);
 }
 
 static void _makeClockwise(spFloatArray *polygon) {
-	int i, n, lastX;
-	float *vertices = polygon->items;
-	int verticeslength = polygon->size;
-
-	float area =
-				  vertices[verticeslength - 2] * vertices[1] - vertices[0] * vertices[verticeslength - 1],
-		  p1x, p1y, p2x, p2y;
-	for (i = 0, n = verticeslength - 3; i < n; i += 2) {
-		p1x = vertices[i];
-		p1y = vertices[i + 1];
-		p2x = vertices[i + 2];
-		p2y = vertices[i + 3];
-		area += p1x * p2y - p2x * p1y;
-	}
-	if (area < 0) return;
-
-	for (i = 0, lastX = verticeslength - 2, n = verticeslength >> 1; i < n; i += 2) {
-		float x = vertices[i], y = vertices[i + 1];
-		int other = lastX - i;
-		vertices[i] = vertices[other];
-		vertices[i + 1] = vertices[other + 1];
-		vertices[other] = x;
-		vertices[other + 1] = y;
-	}
+        int i, n, lastX;
+        float *vertices = polygon->items;
+        int verticeslength = polygon->size;
+
+        float area =
+                                  vertices[verticeslength - 2] * vertices[1] - vertices[0] * vertices[verticeslength - 1];
+        for (i = 0, n = verticeslength - 3; i < n; i += 2) {
+                float p1x = vertices[i];
+                float p1y = vertices[i + 1];
+                float p2x = vertices[i + 2];
+                float p2y = vertices[i + 3];
+                area += p1x * p2y - p2x * p1y;
+        }
+        if (area < 0) return;
+
+        for (i = 0, lastX = verticeslength - 2, n = verticeslength >> 1; i < n; i += 2) {
+                float x = vertices[i], y = vertices[i + 1];
+                int other = lastX - i;
+                vertices[i] = vertices[other];
+                vertices[i + 1] = vertices[other + 1];
+                vertices[other] = x;
+                vertices[other + 1] = y;
+        }
 }
 
 int spSkeletonClipping_clipStart(spSkeletonClipping *self, spSlot *slot, spClippingAttachment *clip) {
-	int i, n;
-	float *vertices;
-	if (self->clipAttachment) return 0;
-	self->clipAttachment = clip;
-
-	n = clip->super.worldVerticesLength;
-	vertices = spFloatArray_setSize(self->clippingPolygon, n)->items;
-	spVertexAttachment_computeWorldVertices(SUPER(clip), slot, 0, n, vertices, 0, 2);
-	_makeClockwise(self->clippingPolygon);
-	self->clippingPolygons = spTriangulator_decompose(self->triangulator, self->clippingPolygon,
-													  spTriangulator_triangulate(self->triangulator,
-																				 self->clippingPolygon));
-	for (i = 0, n = self->clippingPolygons->size; i < n; i++) {
-		spFloatArray *polygon = self->clippingPolygons->items[i];
-		_makeClockwise(polygon);
-		spFloatArray_add(polygon, polygon->items[0]);
-		spFloatArray_add(polygon, polygon->items[1]);
-	}
-	return self->clippingPolygons->size;
+        int i, n;
+        float *vertices;
+        if (self->clipAttachment) return 0;
+        self->clipAttachment = clip;
+
+        n = clip->super.worldVerticesLength;
+        vertices = spFloatArray_setSize(self->clippingPolygon, n)->items;
+        spVertexAttachment_computeWorldVertices(SUPER(clip), slot, 0, n, vertices, 0, 2);
+        _makeClockwise(self->clippingPolygon);
+        self->clippingPolygons = spTriangulator_decompose(self->triangulator, self->clippingPolygon,
+                                                                                                          spTriangulator_triangulate(self->triangulator,
+                                                                                                                                                                 self->clippingPolygon));
+        for (i = 0, n = self->clippingPolygons->size; i < n; i++) {
+                spFloatArray *polygon = self->clippingPolygons->items[i];
+                _makeClockwise(polygon);
+                spFloatArray_add(polygon, polygon->items[0]);
+                spFloatArray_add(polygon, polygon->items[1]);
+        }
+        return self->clippingPolygons->size;
 }
 
 void spSkeletonClipping_clipEnd(spSkeletonClipping *self, spSlot *slot) {
-	if (self->clipAttachment != 0 && self->clipAttachment->endSlot == slot->data) spSkeletonClipping_clipEnd2(self);
+        if (self->clipAttachment != 0 && self->clipAttachment->endSlot == slot->data) spSkeletonClipping_clipEnd2(self);
 }
 
 void spSkeletonClipping_clipEnd2(spSkeletonClipping *self) {
-	if (!self->clipAttachment) return;
-	self->clipAttachment = 0;
-	self->clippingPolygons = 0;
-	spFloatArray_clear(self->clippedVertices);
-	spFloatArray_clear(self->clippedUVs);
-	spUnsignedShortArray_clear(self->clippedTriangles);
-	spFloatArray_clear(self->clippingPolygon);
+        if (!self->clipAttachment) return;
+        self->clipAttachment = 0;
+        self->clippingPolygons = 0;
+        spFloatArray_clear(self->clippedVertices);
+        spFloatArray_clear(self->clippedUVs);
+        spUnsignedShortArray_clear(self->clippedTriangles);
+        spFloatArray_clear(self->clippingPolygon);
 }
 
 int /*boolean*/ spSkeletonClipping_isClipping(spSkeletonClipping *self) {
-	return self->clipAttachment != 0;
+        return self->clipAttachment != 0;
 }
 
 int /*boolean*/
 _clip(spSkeletonClipping *self, float x1, float y1, float x2, float y2, float x3, float y3, spFloatArray *clippingArea,
-	  spFloatArray *output) {
-	spFloatArray *originalOutput = output;
-	int clipped = 0;
-	float *clippingVertices;
-	int clippingVerticesLast;
-
-	spFloatArray *input = 0;
-	if (clippingArea->size % 4 >= 2) {
-		input = output;
-		output = self->scratch;
-	} else
-		input = self->scratch;
-
-	spFloatArray_clear(input);
-	spFloatArray_add(input, x1);
-	spFloatArray_add(input, y1);
-	spFloatArray_add(input, x2);
-	spFloatArray_add(input, y2);
-	spFloatArray_add(input, x3);
-	spFloatArray_add(input, y3);
-	spFloatArray_add(input, x1);
-	spFloatArray_add(input, y1);
-	spFloatArray_clear(output);
-
-	clippingVerticesLast = clippingArea->size - 4;
-	clippingVertices = clippingArea->items;
-	for (int i = 0;; i += 2) {
-		spFloatArray *temp;
-		float edgeX = clippingVertices[i], edgeY = clippingVertices[i + 1];
-		float ex = edgeX - clippingVertices[i + 2], ey = edgeY - clippingVertices[i + 3];
-
-		int outputStart = output->size;
-		float *inputVertices = input->items;
-		for (int ii = 0, nn = input->size - 2; ii < nn;) {
-			float inputX = inputVertices[ii], inputY = inputVertices[ii + 1];
-			ii += 2;
-			float inputX2 = inputVertices[ii], inputY2 = inputVertices[ii + 1];
-			float s2 = ey * (edgeX - inputX2) > ex * (edgeY - inputY2);
-			float s1 = ey * (edgeX - inputX) - ex * (edgeY - inputY);
-			if (s1 > 0) {
-				if (s2) {// v1 inside, v2 inside
-					spFloatArray_add(output, inputX2);
-					spFloatArray_add(output, inputY2);
-					continue;
-				}
-				// v1 inside, v2 outside
-				float ix = inputX2 - inputX, iy = inputY2 - inputY, t = s1 / (ix * ey - iy * ex);
-				if (t >= 0 && t <= 1) {
-					spFloatArray_add(output, inputX + ix * t);
-					spFloatArray_add(output, inputY + iy * t);
-				} else {
-					spFloatArray_add(output, inputX2);
-					spFloatArray_add(output, inputY2);
-				}
-			} else if (s2) {// v1 outside, v2 inside
-				float ix = inputX2 - inputX, iy = inputY2 - inputY, t = s1 / (ix * ey - iy * ex);
-				if (t >= 0 && t <= 1) {
-					spFloatArray_add(output, inputX + ix * t);
-					spFloatArray_add(output, inputY + iy * t);
-					spFloatArray_add(output, inputX2);
-					spFloatArray_add(output, inputY2);
-				} else {
-					spFloatArray_add(output, inputX2);
-					spFloatArray_add(output, inputY2);
-					continue;
-				}
-			}
-			clipped = -1;
-		}
-
-		if (outputStart == output->size) {
-			spFloatArray_clear(originalOutput);
-			return 1;
-		}
-
-		spFloatArray_add(output, output->items[0]);
-		spFloatArray_add(output, output->items[1]);
-
-		if (i == clippingVerticesLast) break;
-		temp = output;
-		output = input;
-		spFloatArray_clear(output);
-		input = temp;
-	}
-
-	if (originalOutput != output) {
-		spFloatArray_clear(originalOutput);
-		spFloatArray_addAllValues(originalOutput, output->items, 0, output->size - 2);
-	} else
-		spFloatArray_setSize(originalOutput, originalOutput->size - 2);
-
-	return clipped;
+          spFloatArray *output) {
+        spFloatArray *originalOutput = output;
+        int clipped = 0;
+        float *clippingVertices;
+        int clippingVerticesLast;
+
+        spFloatArray *input = 0;
+        if (clippingArea->size % 4 >= 2) {
+                input = output;
+                output = self->scratch;
+        } else
+                input = self->scratch;
+
+        spFloatArray_clear(input);
+        spFloatArray_add(input, x1);
+        spFloatArray_add(input, y1);
+        spFloatArray_add(input, x2);
+        spFloatArray_add(input, y2);
+        spFloatArray_add(input, x3);
+        spFloatArray_add(input, y3);
+        spFloatArray_add(input, x1);
+        spFloatArray_add(input, y1);
+        spFloatArray_clear(output);
+
+        clippingVerticesLast = clippingArea->size - 4;
+        clippingVertices = clippingArea->items;
+        for (int i = 0;; i += 2) {
+                spFloatArray *temp;
+                float edgeX = clippingVertices[i], edgeY = clippingVertices[i + 1];
+                float ex = edgeX - clippingVertices[i + 2], ey = edgeY - clippingVertices[i + 3];
+
+                int outputStart = output->size;
+                float *inputVertices = input->items;
+                for (int ii = 0, nn = input->size - 2; ii < nn;) {
+                        float inputX = inputVertices[ii], inputY = inputVertices[ii + 1];
+                        ii += 2;
+                        float inputX2 = inputVertices[ii], inputY2 = inputVertices[ii + 1];
+                        float s2 = ey * (edgeX - inputX2) > ex * (edgeY - inputY2);
+                        float s1 = ey * (edgeX - inputX) - ex * (edgeY - inputY);
+                        if (s1 > 0) {
+                                if (s2) {// v1 inside, v2 inside
+                                        spFloatArray_add(output, inputX2);
+                                        spFloatArray_add(output, inputY2);
+                                        continue;
+                                }
+                                // v1 inside, v2 outside
+                                float ix = inputX2 - inputX, iy = inputY2 - inputY, t = s1 / (ix * ey - iy * ex);
+                                if (t >= 0 && t <= 1) {
+                                        spFloatArray_add(output, inputX + ix * t);
+                                        spFloatArray_add(output, inputY + iy * t);
+                                } else {
+                                        spFloatArray_add(output, inputX2);
+                                        spFloatArray_add(output, inputY2);
+                                }
+                        } else if (s2) {// v1 outside, v2 inside
+                                float ix = inputX2 - inputX, iy = inputY2 - inputY, t = s1 / (ix * ey - iy * ex);
+                                if (t >= 0 && t <= 1) {
+                                        spFloatArray_add(output, inputX + ix * t);
+                                        spFloatArray_add(output, inputY + iy * t);
+                                        spFloatArray_add(output, inputX2);
+                                        spFloatArray_add(output, inputY2);
+                                } else {
+                                        spFloatArray_add(output, inputX2);
+                                        spFloatArray_add(output, inputY2);
+                                        continue;
+                                }
+                        }
+                        clipped = -1;
+                }
+
+                if (outputStart == output->size) {
+                        spFloatArray_clear(originalOutput);
+                        return 1;
+                }
+
+                spFloatArray_add(output, output->items[0]);
+                spFloatArray_add(output, output->items[1]);
+
+                if (i == clippingVerticesLast) break;
+                temp = output;
+                output = input;
+                spFloatArray_clear(output);
+                input = temp;
+        }
+
+        if (originalOutput != output) {
+                spFloatArray_clear(originalOutput);
+                spFloatArray_addAllValues(originalOutput, output->items, 0, output->size - 2);
+        } else
+                spFloatArray_setSize(originalOutput, originalOutput->size - 2);
+
+        return clipped;
 }
 
 void spSkeletonClipping_clipTriangles(spSkeletonClipping *self, float *vertices, int verticesLength,
-									  unsigned short *triangles, int trianglesLength, float *uvs, int stride) {
-	int i;
-	spFloatArray *clipOutput = self->clipOutput;
-	spFloatArray *clippedVertices = self->clippedVertices;
-	spFloatArray *clippedUVs = self->clippedUVs;
-	spUnsignedShortArray *clippedTriangles = self->clippedTriangles;
-	spFloatArray **polygons = self->clippingPolygons->items;
-	int polygonsCount = self->clippingPolygons->size;
-
-	short index = 0;
-	spFloatArray_clear(clippedVertices);
-	spFloatArray_clear(clippedUVs);
-	spUnsignedShortArray_clear(clippedTriangles);
-	i = 0;
+                                                                          unsigned short *triangles, int trianglesLength, float *uvs, int stride) {
+        int i;
+        spFloatArray *clipOutput = self->clipOutput;
+        spFloatArray *clippedVertices = self->clippedVertices;
+        spFloatArray *clippedUVs = self->clippedUVs;
+        spUnsignedShortArray *clippedTriangles = self->clippedTriangles;
+        spFloatArray **polygons = self->clippingPolygons->items;
+        int polygonsCount = self->clippingPolygons->size;
+
+        short index = 0;
+        spFloatArray_clear(clippedVertices);
+        spFloatArray_clear(clippedUVs);
+        spUnsignedShortArray_clear(clippedTriangles);
+        i = 0;
 continue_outer:
-	for (; i < trianglesLength; i += 3) {
-		int p;
-		int vertexOffset = triangles[i] * stride;
-		float x2, y2, u2, v2, x3, y3, u3, v3;
-		float x1 = vertices[vertexOffset], y1 = vertices[vertexOffset + 1];
-		float u1 = uvs[vertexOffset], v1 = uvs[vertexOffset + 1];
-
-		vertexOffset = triangles[i + 1] * stride;
-		x2 = vertices[vertexOffset];
-		y2 = vertices[vertexOffset + 1];
-		u2 = uvs[vertexOffset];
-		v2 = uvs[vertexOffset + 1];
-
-		vertexOffset = triangles[i + 2] * stride;
-		x3 = vertices[vertexOffset];
-		y3 = vertices[vertexOffset + 1];
-		u3 = uvs[vertexOffset];
-		v3 = uvs[vertexOffset + 1];
-
-		for (p = 0; p < polygonsCount; p++) {
-			int s = clippedVertices->size;
-			if (_clip(self, x1, y1, x2, y2, x3, y3, polygons[p], clipOutput)) {
-				int ii;
-				float d0, d1, d2, d4, d;
-				unsigned short *clippedTrianglesItems;
-				int clipOutputCount;
-				float *clipOutputItems;
-				float *clippedVerticesItems;
-				float *clippedUVsItems;
-
-				int clipOutputLength = clipOutput->size;
-				if (clipOutputLength == 0) continue;
-				d0 = y2 - y3;
-				d1 = x3 - x2;
-				d2 = x1 - x3;
-				d4 = y3 - y1;
-				d = 1 / (d0 * d2 + d1 * (y1 - y3));
-
-				clipOutputCount = clipOutputLength >> 1;
-				clipOutputItems = clipOutput->items;
-				clippedVerticesItems = spFloatArray_setSize(clippedVertices, s + (clipOutputCount << 1))->items;
-				clippedUVsItems = spFloatArray_setSize(clippedUVs, s + (clipOutputCount << 1))->items;
-				for (ii = 0; ii < clipOutputLength; ii += 2) {
-					float c0, c1, a, b, c;
-					float x = clipOutputItems[ii], y = clipOutputItems[ii + 1];
-					clippedVerticesItems[s] = x;
-					clippedVerticesItems[s + 1] = y;
-					c0 = x - x3;
-					c1 = y - y3;
-					a = (d0 * c0 + d1 * c1) * d;
-					b = (d4 * c0 + d2 * c1) * d;
-					c = 1 - a - b;
-					clippedUVsItems[s] = u1 * a + u2 * b + u3 * c;
-					clippedUVsItems[s + 1] = v1 * a + v2 * b + v3 * c;
-					s += 2;
-				}
-
-				s = clippedTriangles->size;
-				clippedTrianglesItems = spUnsignedShortArray_setSize(clippedTriangles,
-																	 s + 3 * (clipOutputCount - 2))
-												->items;
-				clipOutputCount--;
-				for (ii = 1; ii < clipOutputCount; ii++) {
-					clippedTrianglesItems[s] = index;
-					clippedTrianglesItems[s + 1] = (unsigned short) (index + ii);
-					clippedTrianglesItems[s + 2] = (unsigned short) (index + ii + 1);
-					s += 3;
-				}
-				index += clipOutputCount + 1;
-
-			} else {
-				unsigned short *clippedTrianglesItems;
-				float *clippedVerticesItems = spFloatArray_setSize(clippedVertices, s + (3 << 1))->items;
-				float *clippedUVsItems = spFloatArray_setSize(clippedUVs, s + (3 << 1))->items;
-				clippedVerticesItems[s] = x1;
-				clippedVerticesItems[s + 1] = y1;
-				clippedVerticesItems[s + 2] = x2;
-				clippedVerticesItems[s + 3] = y2;
-				clippedVerticesItems[s + 4] = x3;
-				clippedVerticesItems[s + 5] = y3;
-
-				clippedUVsItems[s] = u1;
-				clippedUVsItems[s + 1] = v1;
-				clippedUVsItems[s + 2] = u2;
-				clippedUVsItems[s + 3] = v2;
-				clippedUVsItems[s + 4] = u3;
-				clippedUVsItems[s + 5] = v3;
-
-				s = clippedTriangles->size;
-				clippedTrianglesItems = spUnsignedShortArray_setSize(clippedTriangles, s + 3)->items;
-				clippedTrianglesItems[s] = index;
-				clippedTrianglesItems[s + 1] = (unsigned short) (index + 1);
-				clippedTrianglesItems[s + 2] = (unsigned short) (index + 2);
-				index += 3;
-				i += 3;
-				goto continue_outer;
-			}
-		}
-	}
-	UNUSED(verticesLength);
-}
+        for (; i < trianglesLength; i += 3) {
+                int p;
+                int vertexOffset = triangles[i] * stride;
+                float x2, y2, u2, v2, x3, y3, u3, v3;
+                float x1 = vertices[vertexOffset], y1 = vertices[vertexOffset + 1];
+                float u1 = uvs[vertexOffset], v1 = uvs[vertexOffset + 1];
+
+                vertexOffset = triangles[i + 1] * stride;
+                x2 = vertices[vertexOffset];
+                y2 = vertices[vertexOffset + 1];
+                u2 = uvs[vertexOffset];
+                v2 = uvs[vertexOffset + 1];
+
+                vertexOffset = triangles[i + 2] * stride;
+                x3 = vertices[vertexOffset];
+                y3 = vertices[vertexOffset + 1];
+                u3 = uvs[vertexOffset];
+                v3 = uvs[vertexOffset + 1];
+
+                for (p = 0; p < polygonsCount; p++) {
+                        int s = clippedVertices->size;
+                        if (_clip(self, x1, y1, x2, y2, x3, y3, polygons[p], clipOutput)) {
+                                int ii;
+                                float d0, d1, d2, d4, d;
+                                unsigned short *clippedTrianglesItems;
+                                int clipOutputCount;
+                                float *clipOutputItems;
+                                float *clippedVerticesItems;
+                                float *clippedUVsItems;
+
+                                int clipOutputLength = clipOutput->size;
+                                if (clipOutputLength == 0) continue;
+                                d0 = y2 - y3;
+                                d1 = x3 - x2;
+                                d2 = x1 - x3;
+                                d4 = y3 - y1;
+                                d = 1 / (d0 * d2 + d1 * (y1 - y3));
+
+                                clipOutputCount = clipOutputLength >> 1;
+                                clipOutputItems = clipOutput->items;
+                                clippedVerticesItems = spFloatArray_setSize(clippedVertices, s + (clipOutputCount << 1))->items;
+                                clippedUVsItems = spFloatArray_setSize(clippedUVs, s + (clipOutputCount << 1))->items;
+                                for (ii = 0; ii < clipOutputLength; ii += 2) {
+                                        float c0, c1, a, b, c;
+                                        float x = clipOutputItems[ii], y = clipOutputItems[ii + 1];
+                                        clippedVerticesItems[s] = x;
+                                        clippedVerticesItems[s + 1] = y;
+                                        c0 = x - x3;
+                                        c1 = y - y3;
+                                        a = (d0 * c0 + d1 * c1) * d;
+                                        b = (d4 * c0 + d2 * c1) * d;
+                                        c = 1 - a - b;
+                                        clippedUVsItems[s] = u1 * a + u2 * b + u3 * c;
+                                        clippedUVsItems[s + 1] = v1 * a + v2 * b + v3 * c;
+                                        s += 2;
+                                }
+
+                                s = clippedTriangles->size;
+                                clippedTrianglesItems = spUnsignedShortArray_setSize(clippedTriangles,
+                                                                                                                                         s + 3 * (clipOutputCount - 2))
+                                                                                                ->items;
+                                clipOutputCount--;
+                                for (ii = 1; ii < clipOutputCount; ii++) {
+                                        clippedTrianglesItems[s] = index;
+                                        clippedTrianglesItems[s + 1] = (unsigned short) (index + ii);
+                                        clippedTrianglesItems[s + 2] = (unsigned short) (index + ii + 1);
+                                        s += 3;
+                                }
+                                index += clipOutputCount + 1;
+
+                        } else {
+                                unsigned short *clippedTrianglesItems;
+                                float *clippedVerticesItems = spFloatArray_setSize(clippedVertices, s + (3 << 1))->items;
+                                float *clippedUVsItems = spFloatArray_setSize(clippedUVs, s + (3 << 1))->items;
+                                clippedVerticesItems[s] = x1;
+                                clippedVerticesItems[s + 1] = y1;
+                                clippedVerticesItems[s + 2] = x2;
+                                clippedVerticesItems[s + 3] = y2;
+                                clippedVerticesItems[s + 4] = x3;
+                                clippedVerticesItems[s + 5] = y3;
+
+                                clippedUVsItems[s] = u1;
+                                clippedUVsItems[s + 1] = v1;
+                                clippedUVsItems[s + 2] = u2;
+                                clippedUVsItems[s + 3] = v2;
+                                clippedUVsItems[s + 4] = u3;
+                                clippedUVsItems[s + 5] = v3;
+
+                                s = clippedTriangles->size;
+                                clippedTrianglesItems = spUnsignedShortArray_setSize(clippedTriangles, s + 3)->items;
+                                clippedTrianglesItems[s] = index;
+                                clippedTrianglesItems[s + 1] = (unsigned short) (index + 1);
+                                clippedTrianglesItems[s + 2] = (unsigned short) (index + 2);
+                                index += 3;
+                                i += 3;
+                                goto continue_outer;
+                        }
+                }
+        }
+        UNUSED(verticesLength);
+}


```

---

## [9/50] ID: CPP_0220 | C/C++ (F)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `LINTER_FAIL`
- **Target File:** `services/service/src/device_manager_service_listener.cpp`
- **Warning:** Consider using std::find_if algorithm instead of a raw loop.

### Buggy Snippet
```cpp
int32_t DeviceManagerServiceListener::OnServiceInfoChange(const DmRegisterServiceState &registerServiceState,
    const DmServiceInfo &serviceInfo)
{
    LOGI("OnServiceInfoChange start.");
    std::shared_ptr<IpcNotifyServiceStateReq> pReq = std::make_shared<IpcNotifyServiceStateReq>();
    std::shared_ptr<IpcRsp> pRsp = std::make_shared<IpcRsp>();
    std::string notifyPkgName = registerServiceState.pkgName;
    pReq->SetDmRegisterServiceState(registerServiceState);
    pReq->SetDmServiceInfo(serviceInfo);
    pReq->SetServiceState(DmServiceState::SERVICE_INFO_CHANGED);
    std::vector<ProcessInfo> processInfos = ipcServerListener_.GetAllProcessInfo();
    ProcessInfo processInfoTemp;
    for (const auto &item : processInfos) {
        if (item.pkgName == registerServiceState.pkgName && item.userId == registerServiceState.userId) {
            processInfoTemp = item;
            break;
        }
    }
    if (processInfoTemp.pkgName.empty()) {
        LOGI("not register listener");
        return ERR_DM_FAILED;
    }
    pReq->SetPkgName(processInfoTemp.pkgName);
    pReq->SetProcessInfo(processInfoTemp);
    int32_t ret = ipcServerListener_.SendRequest(SERVER_SERVICE_STATE_NOTIFY, pReq, pRsp);
    if (ret != DM_OK) {
        LOGE("OnServiceInfoChange failed.");
        return ret;
    }
    return DM_OK;
}
```

### Patch
```diff
// File: services/service/src/device_manager_service_listener.cpp
--- a/services/service/src/device_manager_service_listener.cpp
+++ b/services/service/src/device_manager_service_listener.cpp
@@ -13,6 +13,7 @@
  * limitations under the License.
  */
 
+#include <algorithm>
 #include <set>
 #include <sstream>
 #include "cJSON.h"
@@ -1408,11 +1409,12 @@
     pReq->SetServiceState(DmServiceState::SERVICE_INFO_CHANGED);
     std::vector<ProcessInfo> processInfos = ipcServerListener_.GetAllProcessInfo();
     ProcessInfo processInfoTemp;
-    for (const auto &item : processInfos) {
-        if (item.pkgName == registerServiceState.pkgName && item.userId == registerServiceState.userId) {
-            processInfoTemp = item;
-            break;
-        }
+    auto it = std::find_if(processInfos.begin(), processInfos.end(),
+        [&registerServiceState](const auto &item) {
+            return item.pkgName == registerServiceState.pkgName && item.userId == registerServiceState.userId;
+        });
+    if (it != processInfos.end()) {
+        processInfoTemp = *it;
     }
     if (processInfoTemp.pkgName.empty()) {
         LOGI("not register listener");


```

---

## [10/50] ID: CPP_0030 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `napi/settings/napi_settings.cpp`
- **Warning:** Function parameter 'tableName' should be passed by const reference.

### Buggy Snippet
```cpp
// get proxy uri
std::string GetProxyUriStr(std::string tableName, int id)
{
    if (id < USERID_HELPER_NUMBER) {
        id = USERID_HELPER_NUMBER;
    }
    std::string idStr = std::to_string(id);
    if (tableName == "global") {
        // return global uri
        std::string retStr = "datashare:///com.ohos.settingsdata/entry/settingsdata/SETTINGSDATA?Proxy=true";
        return retStr;
    } else if (tableName == "system") {
        std::string retStr =
            "datashare:///com.ohos.settingsdata/entry/settingsdata/USER_SETTINGSDATA_" + idStr + "?Proxy=true";
        return retStr;
    } else {
        std::string retStr =
            "datashare:///com.ohos.settingsdata/entry/settingsdata/USER_SETTINGSDATA_SECURE_" + idStr + "?Proxy=true";
        return retStr;
    }
}
```

### Patch
```diff
// File: napi/settings/napi_settings.cpp
--- a/napi/settings/napi_settings.cpp
+++ b/napi/settings/napi_settings.cpp
@@ -420,7 +420,7 @@
     return dataShareHelper;
 }
 
-std::shared_ptr<DataShareHelper> getDataShareHelper(napi_env env, sptr<IRemoteObject> token, std::string tableName,
+std::shared_ptr<DataShareHelper> getDataShareHelper(napi_env env, sptr<IRemoteObject> token, const std::string& tableName,
                                                     AsyncCallbackInfo *asyncCallbackInfo)
 {
     if (globalDataShareHelper != nullptr) {
@@ -1410,7 +1410,7 @@
     if (wrapper != nullptr) {
         asyncCallbackInfo->dataAbilityHelper = wrapper->GetDataAbilityHelper();
     }
-	
+        
     asyncCallbackInfo->key = unwrap_string_from_js(env, args[PARAM1]);
     asyncCallbackInfo->value = unwrap_string_from_js(env, args[PARAM2]);
     SETTING_LOG_INFO("set  input param is : (key %{public}s, value %{public}s)",
@@ -1860,7 +1860,7 @@
 }
 
 // get uri for stage model
-std::string GetStageUriStr(std::string tableName, int id, std::string keyStr)
+std::string GetStageUriStr(const std::string& tableName, int id, const std::string& keyStr)
 {
     if (id < USERID_HELPER_NUMBER) {
         id = USERID_HELPER_NUMBER;
@@ -1887,7 +1887,7 @@
 }
 
 // get proxy uri
-std::string GetProxyUriStr(std::string tableName, int id)
+std::string GetProxyUriStr(const std::string& tableName, int id)
 {
     if (id < USERID_HELPER_NUMBER) {
         id = USERID_HELPER_NUMBER;
@@ -1909,7 +1909,7 @@
 }
 
 // check whether tableName is invalid, invalid -> true valid -> false
-bool IsTableNameInvalid(std::string tableName)
+bool IsTableNameInvalid(const std::string& tableName)
 {
     if (tableName != "global" && tableName != "system" && tableName != "secure") {
         return true;


```

---

## [11/50] ID: CPP_0132 | C/C++ (F)
- **Rule ID:** `cppcheck/variableScope`
- **Result:** `LINTER_FAIL`
- **Target File:** `spinec/Spinec/src/main/cpp/thirdparty/stb/stb_image.h`
- **Warning:** The scope of the variable 't0' can be reduced.

### Buggy Snippet
```cpp
#define stbi__div16(x) ((stbi_uc) ((x) >> 4))

static stbi_uc *stbi__resample_row_hv_2(stbi_uc *out, stbi_uc *in_near, stbi_uc *in_far, int w, int hs)
{
   int i,t0,t1;
   if (w == 1) {
      out[0] = out[1] = stbi__div4(3*in_near[0] + in_far[0] + 2);
      return out;
   }

   t1 = 3*in_near[0] + in_far[0];
   out[0] = stbi__div4(t1+2);
   for (i=1; i < w; ++i) {
      t0 = t1;
      t1 = 3*in_near[i]+in_far[i];
      out[i*2-1] = stbi__div16(3*t0 + t1 + 8);
      out[i*2  ] = stbi__div16(3*t1 + t0 + 8);
   }
   out[w*2-1] = stbi__div4(t1+2);

   STBI_NOTUSED(hs);

   return out;
}
```

### Patch
```diff
// File: spinec/Spinec/src/main/cpp/thirdparty/stb/stb_image.h
--- a/spinec/Spinec/src/main/cpp/thirdparty/stb/stb_image.h
+++ b/spinec/Spinec/src/main/cpp/thirdparty/stb/stb_image.h
@@ -851,7 +851,7 @@
 #if defined(_WIN32) && defined(STBI_WINDOWS_UTF8)
 STBIDEF int stbi_convert_wchar_to_utf8(char *buffer, size_t bufferlen, const wchar_t* input)
 {
-	return WideCharToMultiByte(65001 /* UTF8 */, 0, input, -1, buffer, (int) bufferlen, NULL, NULL);
+        return WideCharToMultiByte(65001 /* UTF8 */, 0, input, -1, buffer, (int) bufferlen, NULL, NULL);
 }
 #endif
 
@@ -861,15 +861,15 @@
 #if defined(_WIN32) && defined(STBI_WINDOWS_UTF8)
    wchar_t wMode[64];
    wchar_t wFilename[1024];
-	if (0 == MultiByteToWideChar(65001 /* UTF8 */, 0, filename, -1, wFilename, sizeof(wFilename)/sizeof(*wFilename)))
+        if (0 == MultiByteToWideChar(65001 /* UTF8 */, 0, filename, -1, wFilename, sizeof(wFilename)/sizeof(*wFilename)))
       return 0;
 
-	if (0 == MultiByteToWideChar(65001 /* UTF8 */, 0, mode, -1, wMode, sizeof(wMode)/sizeof(*wMode)))
+        if (0 == MultiByteToWideChar(65001 /* UTF8 */, 0, mode, -1, wMode, sizeof(wMode)/sizeof(*wMode)))
       return 0;
 
 #if defined(_MSC_VER) && _MSC_VER >= 1400
-	if (0 != _wfopen_s(&f, wFilename, wMode))
-		f = 0;
+        if (0 != _wfopen_s(&f, wFilename, wMode))
+                f = 0;
 #else
    f = _wfopen(wFilename, wMode);
 #endif
@@ -2777,7 +2777,7 @@
 
 static stbi_uc *stbi__resample_row_hv_2(stbi_uc *out, stbi_uc *in_near, stbi_uc *in_far, int w, int hs)
 {
-   int i,t0,t1;
+   int i,t1;
    if (w == 1) {
       out[0] = out[1] = stbi__div4(3*in_near[0] + in_far[0] + 2);
       return out;
@@ -2786,7 +2786,7 @@
    t1 = 3*in_near[0] + in_far[0];
    out[0] = stbi__div4(t1+2);
    for (i=1; i < w; ++i) {
-      t0 = t1;
+      int t0 = t1;
       t1 = 3*in_near[i]+in_far[i];
       out[i*2-1] = stbi__div16(3*t0 + t1 + 8);
       out[i*2  ] = stbi__div16(3*t1 + t0 + 8);
@@ -4438,7 +4438,7 @@
    stbi__png p;
    p.s = s;
    if (!stbi__png_info_raw(&p, NULL, NULL, NULL))
-	   return 0;
+           return 0;
    if (p.depth != 16) {
       stbi__rewind(p.s);
       return 0;
@@ -6523,7 +6523,7 @@
 static int stbi__pnm_is16(stbi__context *s)
 {
    if (stbi__pnm_info(s, NULL, NULL, NULL) == 16)
-	   return 1;
+           return 1;
    return 0;
 }
 #endif


```

---

## [12/50] ID: CPP_0351 | C/C++ (F)
- **Rule ID:** `cppcheck/uninitvar`
- **Result:** `LINTER_FAIL`
- **Target File:** `library/src/main/cpp/napi/http2_common.h`
- **Warning:** Uninitialized variables: sendDataResult.wantIo, sendDataResult.fd, sendDataResult.writeBuffLen, sendDataResult.callbacks, sendDataResult.buffer

### Buggy Snippet
```cpp
Connection SendData(Connection *connection, void *bufferData, int buffLen, string extendParams)
{
    LOGE("napi-->SendData reqId %s host %s path %s buffLen %d rpcType %d", connection->reqId.c_str(),
         connection->host.c_str(), connection->path.c_str(), buffLen, connection->rpcType);
    std::unordered_map<std::string, std::string> parseHeadersMap = ParseReqExtendParams(extendParams);
    std::vector<nghttp2_nv> nva = RequestHeader(connection->host, connection->path);
    bool dataFlags = false;
    bool recvLargeDataFlags = false;
    for (const auto &header : parseHeadersMap) {
        const std::string key = header.first;
        const std::string value = header.second;
        LOGE("SendData header key %s value %s", key.c_str(), value.c_str());
        if (CheckStringIsArray(value)) {
            const std::string valueTemp = GetFirstIndexFromArray(value);
            if (key == "dataflags") {
                dataFlags = NapiUtil::StringToBool(valueTemp);
            }
            if (key == "recvlargedataflags") {
                recvLargeDataFlags = NapiUtil::StringToBool(valueTemp);
            }
            nva.push_back(CreateNV(key.c_str(), valueTemp.c_str()));
        } else {
            nva.push_back(CreateNV(key.c_str(), value.c_str()));
        }
    }
    Connection sendDataResult;
    if (!connection->session || !CheckReqId(&connection->reqId)) {
        LOGE("Error SendData session %p  reqId %s ", connection->session, connection->reqId.c_str());
        return sendDataResult;
    }
    nghttp2_data_source reqBuffer;
    reqBuffer.ptr = bufferData;
    nghttp2_data_provider2 data_prvd = {reqBuffer, DataSourceReadCallback};
    connection->writeBuffLen = buffLen;
    connection->dataFlags = dataFlags;
    connection->buffer = static_cast<uint8_t *>(bufferData);
    connection->canSendData = true;
    connection->recvLargeDataFlags = recvLargeDataFlags;
    int streamId = nghttp2_submit_request2(connection->session, nullptr, nva.data(),
        nva.size(), &data_prvd, connection);
    LOGE("SendData end streamId %d", streamId);
    sendDataResult.dataFlags = dataFlags;
    sendDataResult.recvLargeDataFlags = recvLargeDataFlags;
    sendDataResult.streamId = streamId;
    return sendDataResult;
}
```

### Patch
```diff
// File: library/src/main/cpp/napi/http2_common.h
--- a/library/src/main/cpp/napi/http2_common.h
+++ b/library/src/main/cpp/napi/http2_common.h
@@ -380,6 +380,11 @@
         }
     }
     Connection sendDataResult;
+    sendDataResult.wantIo = IO_NONE;
+    sendDataResult.fd = -1;
+    sendDataResult.writeBuffLen = 0;
+    sendDataResult.callbacks = nullptr;
+    sendDataResult.buffer = nullptr;
     if (!connection->session || !CheckReqId(&connection->reqId)) {
         LOGE("Error SendData session %p  reqId %s ", connection->session, connection->reqId.c_str());
         return sendDataResult;


```

---

## [13/50] ID: CPP_0053 | C/C++ (F)
- **Rule ID:** `cppcheck/knownConditionTrueFalse`
- **Result:** `SECONDARY_DEFECT: 4`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/ohos/napi_handler.cpp`
- **Warning:** Condition 'buf.get()==nullptr' is always false

### Buggy Snippet
```cpp
template <>
std::string NapiHandler::ParseArg<std::string>(const napi_value &arg) const
{
    std::string result = "";
    size_t length = 0;

    NAPI_CALL_HANDLE(env_, napi_get_value_string_utf8(env_, arg, nullptr, 0, &length), result);

    if (length == 0) {
        return result;
    }
    if (length < 0) {
        LOGE("%s string too long to malloc failed, %d", __func__, length);
        return result;
    }

    std::unique_ptr<char[]> buf = std::make_unique<char[]>(length + 1);
    if (buf.get() == nullptr) {
        LOGE("%s nullptr js object to string malloc failed", __func__);
        return result;
    }
    std::fill(buf.get(), buf.get() + (length + 1), 0);
    NAPI_CALL_HANDLE(env_, napi_get_value_string_utf8(env_, arg, buf.get(), length + 1, &length), result);
    result = buf.get();
    return result;
}
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/ohos/napi_handler.cpp
--- a/ohos_YYEVA/library/src/main/cpp/ohos/napi_handler.cpp
+++ b/ohos_YYEVA/library/src/main/cpp/ohos/napi_handler.cpp
@@ -176,10 +176,6 @@
     }
 
     std::unique_ptr<char[]> buf = std::make_unique<char[]>(length + 1);
-    if (buf.get() == nullptr) {
-        LOGE("%s nullptr js object to string malloc failed", __func__);
-        return result;
-    }
     std::fill(buf.get(), buf.get() + (length + 1), 0);
     NAPI_CALL_HANDLE(env_, napi_get_value_string_utf8(env_, arg, buf.get(), length + 1, &length), result);
     result = buf.get();


```

---

## [14/50] ID: CPP_0310 | C/C++ (F)
- **Rule ID:** `cppcheck/stlIfStrFind`
- **Result:** `LINTER_FAIL`
- **Target File:** `frameworks/innerkitsimpl/media_library_manager/media_library_manager.cpp`
- **Warning:** Inefficient usage of string::find() in condition; string::starts_with() could be faster.

### Buggy Snippet
```cpp
std::unique_ptr<PixelMap> MediaLibraryManager::GetAstc(const Uri &uri)
{
    // uri is file://media/image/<id>&oper=astc&width=<width>&height=<height>&path=<path>
    MediaLibraryTracer tracer;
    string uriStr = uri.ToString();
    if (uriStr.empty()) {
        MEDIA_ERR_LOG("GetAstc failed, uri is empty");
        return nullptr;
    }
    auto astcIndex = uriStr.find("astc");
    if (astcIndex == string::npos || astcIndex > uriStr.length()) {
        MEDIA_ERR_LOG("GetAstc failed, oper is invalid");
        return nullptr;
    }
    UriParams uriParams;
    if (!GetParamsFromUri(uriStr, false, uriParams)) {
        MEDIA_ERR_LOG("GetAstc failed, get params from uri failed, uri :%{public}s", uriStr.c_str());
        return nullptr;
    }
    tracer.Start("GetAstc uri:" + uriParams.fileUri);
    string openUriStr = uriParams.fileUri + "?" + CONST_MEDIA_OPERN_KEYWORD + "=" +
        CONST_MEDIA_DATA_DB_THUMB_ASTC + "&" + CONST_MEDIA_DATA_DB_WIDTH + "=" + to_string(uriParams.size.width) +
            "&" + CONST_MEDIA_DATA_DB_HEIGHT + "=" + to_string(uriParams.size.height);
    if (uriParams.user != "") {
        openUriStr = openUriStr + "&" + THUMBNAIL_USER + "=" + uriParams.user;
        if (!uriParams.path.empty() && !uriParams.path.find(MULTI_USER_URI_FLAG)) {
            uriParams.path = uriParams.path + "&" + THUMBNAIL_USER + "=" + uriParams.user;
        }
    }
    tracer.Start("MediaLibraryManager::OpenThumbnail");
    UniqueFd uniqueFd(MediaLibraryManager::OpenThumbnail(openUriStr, uriParams.path, uriParams.size, true));
    if (uniqueFd.Get() < 0) {
        MEDIA_ERR_LOG("OpenThumbnail failed, errCode is %{public}d, uri :%{public}s, path :%{public}s",
            uniqueFd.Get(), uriParams.fileUri.c_str(), MediaFileUtils::DesensitizePath(uriParams.path).c_str());
        return nullptr;
    }
    tracer.Finish();
    auto pixelmap = DecodeAstc(uniqueFd);
    if (pixelmap == nullptr) {
        MEDIA_ERR_LOG("pixelmap is null, uri :%{public}s, path :%{public}s",
            uriParams.fileUri.c_str(), MediaFileUtils::DesensitizePath(uriParams.path).c_str());
    }
    return pixelmap;
}
```

### Patch
```diff
// File: frameworks/innerkitsimpl/media_library_manager/media_library_manager.cpp
--- a/frameworks/innerkitsimpl/media_library_manager/media_library_manager.cpp
+++ b/frameworks/innerkitsimpl/media_library_manager/media_library_manager.cpp
@@ -885,7 +885,7 @@
             "&" + CONST_MEDIA_DATA_DB_HEIGHT + "=" + to_string(uriParams.size.height);
     if (uriParams.user != "") {
         openUriStr = openUriStr + "&" + THUMBNAIL_USER + "=" + uriParams.user;
-        if (!uriParams.path.empty() && !uriParams.path.find(MULTI_USER_URI_FLAG)) {
+        if (!uriParams.path.empty() && uriParams.path.find(MULTI_USER_URI_FLAG) == 0) {
             uriParams.path = uriParams.path + "&" + THUMBNAIL_USER + "=" + uriParams.user;
         }
     }


```

---

## [15/50] ID: CPP_0217 | C/C++ (F)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `LINTER_FAIL`
- **Target File:** `services/service/src/device_manager_service_listener.cpp`
- **Warning:** Consider using std::any_of, std::all_of, std::none_of algorithm instead of a raw loop.

### Buggy Snippet
```cpp
void DeviceManagerServiceListener::OnAuthCodeInvalid(const std::string &pkgName, const std::string &consumerPkgName)
{
    LOGI("OnAuthCodeInvalid : %{public}s", pkgName.c_str());
    (void)consumerPkgName;
    if (pkgName.empty()) {
        LOGE("OnAuthCodeInvalid: pkgName is empty, skip IPC request");
        return;
    }
    std::shared_ptr<IpcReq> pReq = std::make_shared<IpcReq>();
    std::shared_ptr<IpcRsp> pRsp = std::make_shared<IpcRsp>();
    std::vector<ProcessInfo> processInfos = ipcServerListener_.GetAllProcessInfo();
    ProcessInfo processInfoTemp;
    for (const auto &item : processInfos) {
        if (item.pkgName == pkgName) {
            processInfoTemp = item;
        }
    }
    if (processInfoTemp.pkgName.empty()) {
        LOGI("not register listener");
        return;
    }
    pReq->SetPkgName(processInfoTemp.pkgName);
    pReq->SetProcessInfo(processInfoTemp);
    ipcServerListener_.SendRequest(ON_AUTH_CODE_INVALID, pReq, pRsp);
}
```

### Patch
```diff
// File: services/service/src/device_manager_service_listener.cpp
--- a/services/service/src/device_manager_service_listener.cpp
+++ b/services/service/src/device_manager_service_listener.cpp
@@ -1296,16 +1296,13 @@
     std::shared_ptr<IpcReq> pReq = std::make_shared<IpcReq>();
     std::shared_ptr<IpcRsp> pRsp = std::make_shared<IpcRsp>();
     std::vector<ProcessInfo> processInfos = ipcServerListener_.GetAllProcessInfo();
-    ProcessInfo processInfoTemp;
-    for (const auto &item : processInfos) {
-        if (item.pkgName == pkgName) {
-            processInfoTemp = item;
-        }
-    }
-    if (processInfoTemp.pkgName.empty()) {
+    auto it = std::find_if(processInfos.begin(), processInfos.end(),
+        [&pkgName](const ProcessInfo &item) { return item.pkgName == pkgName; });
+    if (it == processInfos.end()) {
         LOGI("not register listener");
         return;
     }
+    ProcessInfo processInfoTemp = *it;
     pReq->SetPkgName(processInfoTemp.pkgName);
     pReq->SetProcessInfo(processInfoTemp);
     ipcServerListener_.SendRequest(ON_AUTH_CODE_INVALID, pReq, pRsp);


```

---

## [16/50] ID: CPP_0167 | C/C++ (F)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `LINTER_FAIL`
- **Target File:** `vap/vap_module/src/main/cpp/render/plugin_render.cpp`
- **Warning:** Local variable 'ret' shadows outer variable

### Buggy Snippet
```cpp
static void DispatchTouchEventCB(OH_NativeXComponent *component, void *window)
{
    LOGD("DispatchTouchEventCB");
    if ((nullptr == component) || (nullptr == window)) {
        LOGE("DispatchTouchEventCB: component or window is null");
        return;
    }

    char idStr[OH_XCOMPONENT_ID_LEN_MAX + ONE] = { '\0' };
    uint64_t idSize = OH_XCOMPONENT_ID_LEN_MAX + ONE;
    if (OH_NATIVEXCOMPONENT_RESULT_SUCCESS != OH_NativeXComponent_GetXComponentId(component, idStr, &idSize)) {
        LOGE("DispatchTouchEventCB: Unable to get XComponent id");
        return;
    }
    
    std::string id(idStr);
    auto render = PluginRender::GetInstance(id);
    if (nullptr != render) {
        LOGD("surface touch");
        OH_NativeXComponent_TouchEvent touchEvent;
        int32_t ret = OH_NativeXComponent_GetTouchEvent(component, window, &touchEvent);
        if (ret == OH_NATIVEXCOMPONENT_RESULT_SUCCESS) {
            LOGI("Touch Info : x = %{public}f, y = %{public}f screenx = %{public}f, screeny = %{public}f",
                 touchEvent.x, touchEvent.y, touchEvent.screenX, touchEvent.screenY);
            for (uint32_t i = 0; i < touchEvent.numPoints; i++) {
                LOGI("Touch Info : dots[%{public}d] id %{public}d x = %{public}f, y = %{public}f", i,
                     touchEvent.touchPoints[i].id, touchEvent.touchPoints[i].x, touchEvent.touchPoints[i].y);
                LOGI("Touch Info : screenx = %{public}f, screeny = %{public}f",
                     touchEvent.touchPoints[i].screenX, touchEvent.touchPoints[i].screenY);
                OH_NativeXComponent_TouchPointToolType toolType;
                float tiltX = 0.0;
                float tiltY = 0.0;
                int32_t ret = OH_NativeXComponent_GetTouchPointToolType(component, i, &toolType);
                ret = OH_NativeXComponent_GetTouchPointTiltX(component, i, &tiltX);
                ret = OH_NativeXComponent_GetTouchPointTiltY(component, i, &tiltY);
                LOGI("Touch Info : [%{public}d] %{public}u, %{public}f, %{public}f",
                     i, toolType, tiltX, tiltY);
            }
            render->player_->XComponentClick(touchEvent.x, touchEvent.y);
        } else {
            LOGE("Touch fail");
        }
    }
}
```

### Patch
```diff
// File: vap/vap_module/src/main/cpp/render/plugin_render.cpp
--- a/vap/vap_module/src/main/cpp/render/plugin_render.cpp
+++ b/vap/vap_module/src/main/cpp/render/plugin_render.cpp
@@ -148,9 +148,9 @@
                 OH_NativeXComponent_TouchPointToolType toolType;
                 float tiltX = 0.0;
                 float tiltY = 0.0;
-                int32_t ret = OH_NativeXComponent_GetTouchPointToolType(component, i, &toolType);
-                ret = OH_NativeXComponent_GetTouchPointTiltX(component, i, &tiltX);
-                ret = OH_NativeXComponent_GetTouchPointTiltY(component, i, &tiltY);
+                int32_t result = OH_NativeXComponent_GetTouchPointToolType(component, i, &toolType);
+                result = OH_NativeXComponent_GetTouchPointTiltX(component, i, &tiltX);
+                result = OH_NativeXComponent_GetTouchPointTiltY(component, i, &tiltY);
                 LOGI("Touch Info : [%{public}d] %{public}u, %{public}f, %{public}f",
                      i, toolType, tiltX, tiltY);
             }


```

---

## [17/50] ID: CPP_0181 | C/C++ (F)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `SECONDARY_DEFECT: 3`
- **Target File:** `common/src/dm_anonymous.cpp`
- **Warning:** Consider using std::any_of algorithm instead of a raw loop.

### Buggy Snippet
```cpp
bool IsValueExist(const std::multimap<std::string, int32_t> unorderedmap, const std::string &udid, int32_t userId)
{
    for (const auto &item : unorderedmap) {
        if (item.first == udid && item.second == userId) {
            return true;
        }
    }
    return false;
}
```

### Patch
```diff
// File: common/src/dm_anonymous.cpp
--- a/common/src/dm_anonymous.cpp
+++ b/common/src/dm_anonymous.cpp
@@ -15,6 +15,7 @@
 
 #include "dm_anonymous.h"
 #include "dm_log.h"
+#include <algorithm>
 #include <sstream>
 #include <set>
 
@@ -429,12 +430,10 @@
 
 bool IsValueExist(const std::multimap<std::string, int32_t> unorderedmap, const std::string &udid, int32_t userId)
 {
-    for (const auto &item : unorderedmap) {
-        if (item.first == udid && item.second == userId) {
-            return true;
-        }
-    }
-    return false;
+    return std::any_of(unorderedmap.begin(), unorderedmap.end(),
+        [&udid, userId](const auto &item) {
+            return item.first == udid && item.second == userId;
+        });
 }
 
 bool IsDmCommonNotifyEventValid(DmCommonNotifyEvent dmCommonNotifyEvent)


```

---

## [18/50] ID: CPP_0182 | C/C++ (F)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `SECONDARY_DEFECT: 6`
- **Target File:** `commondependency/src/deviceprofile_connector.cpp`
- **Warning:** Consider using std::any_of algorithm instead of a raw loop.

### Buggy Snippet
```cpp
bool DeviceProfileConnector::CheckAccessControlProfileByTokenId(int32_t tokenId)
{
    if (tokenId < 0) {
        LOGE("tokenId error.");
        return false;
    }
    std::string localUdid = GetLocalDeviceId();
    int32_t userId = MultipleUserConnector::GetCurrentAccountUserID();
    std::vector<AccessControlProfile> profiles = GetAllAccessControlProfile();
    for (const auto &item : profiles) {
        if (IsLnnAcl(item)) {
            continue;
        }
        if (item.GetAccesser().GetAccesserDeviceId() == localUdid &&
            item.GetAccesser().GetAccesserUserId() == userId &&
            static_cast<int32_t>(item.GetAccesser().GetAccesserTokenId()) == tokenId) {
            return true;
        }
        if (item.GetAccessee().GetAccesseeDeviceId() == localUdid &&
            item.GetAccessee().GetAccesseeUserId() == userId &&
            static_cast<int32_t>(item.GetAccessee().GetAccesseeTokenId()) == tokenId) {
            return true;
        }
    }
    return false;
}
```

### Patch
```diff
// File: commondependency/src/deviceprofile_connector.cpp
--- a/commondependency/src/deviceprofile_connector.cpp
+++ b/commondependency/src/deviceprofile_connector.cpp
@@ -13,6 +13,7 @@
  * limitations under the License.
  */
 
+#include <algorithm>
 #include <cstdio>
 
 #include "deviceprofile_connector.h"
@@ -3990,12 +3991,10 @@
         LOGE("bundleName empty.");
         return false;
     }
-    for (uint32_t index = 0 ; index < AUTH_EXT_WHITE_LIST_NUM ; index++) {
-        if (pkgName == g_extWhiteList[index]) {
-            return true;
-        }
-    }
-    return false;
+    return std::any_of(g_extWhiteList, g_extWhiteList + AUTH_EXT_WHITE_LIST_NUM,
+        [&pkgName](const char* whiteListItem) {
+            return pkgName == whiteListItem;
+        });
 }
 
 bool DeviceProfileConnector::IsAllowAuthAlways(const std::string &localUdid, int32_t userId,


```

---

## [19/50] ID: CPP_0017 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `cj/settings/src/cj_settings.cpp`
- **Warning:** Function parameter 'setValue' should be passed by const reference.

### Buggy Snippet
```cpp
bool SetValueExecuteExt(SettingsInfo* info, const std::string setValue, int32_t* ret)
{
    if (info->dataShareHelper == nullptr) {
        LOGE("helper is null");
        *ret = 0;
        return false;
    }
    OHOS::DataShare::DataShareValuesBucket val;
    val.Put(SETTINGS_DATA_FIELD_KEYWORD, info->key);
    val.Put(SETTINGS_DATA_FIELD_VALUE, setValue);
    std::string tmpIdStr = GetUserIdStr();
    std::string strUri = GetStageUriStr(info->tableName, tmpIdStr, info->key);
    LOGD("Set uri : %{public}s, key: %{public}s", strUri.c_str(), info->key.c_str());
    OHOS::Uri uri(strUri);

    OHOS::DataShare::DataSharePredicates predicates;
    predicates.EqualTo(SETTINGS_DATA_FIELD_KEYWORD, info->key);

    int32_t retInt = info->dataShareHelper->Update(uri, predicates, val);
    LOGD("update ret: %{public}d", retInt);
    if (retInt <= 0) {
        retInt = info->dataShareHelper->Insert(uri, val);
        LOGD("insert ret: %{public}d", retInt);
    }
    return CheckoutStatus(retInt, ret);
}
```

### Patch
```diff
// File: cj/settings/src/cj_settings.cpp
--- a/cj/settings/src/cj_settings.cpp
+++ b/cj/settings/src/cj_settings.cpp
@@ -127,7 +127,7 @@
     }
 }
 
-bool SetValueExecuteExt(SettingsInfo* info, const std::string setValue, int32_t* ret)
+bool SetValueExecuteExt(SettingsInfo* info, const std::string& setValue, int32_t* ret)
 {
     if (info->dataShareHelper == nullptr) {
         LOGE("helper is null");


```

---

## [20/50] ID: CPP_0002 | C/C++ (F)
- **Rule ID:** `cppcheck/knownConditionTrueFalse`
- **Result:** `SECONDARY_DEFECT: 11`
- **Target File:** `ani/settings/ani_settings.cpp`
- **Warning:** Condition 'asyncCallbackInfo!=nullptr' is always true

### Buggy Snippet
```cpp
ani_boolean ani_can_show_floating(ani_env *env)
{
    AsyncCallbackInfo *asyncCallbackInfo = new AsyncCallbackInfo{
        .env = env,
        .callbackRef = nullptr,
        .dataAbilityHelper = nullptr,
        .key = "",
        .value = "",
        .uri = "",
        .status = 0,
    };
    if (asyncCallbackInfo == nullptr) {
        SETTING_LOG_ERROR("asyncCallbackInfo is null");
        return false;
    }
    ThrowExistingError(env, UNSUPPORT_CODE, "");
    if (asyncCallbackInfo != nullptr) {
        delete asyncCallbackInfo;
        asyncCallbackInfo = nullptr;
    }
    return true;
}
```

### Patch
```diff
// File: ani/settings/ani_settings.cpp
--- a/ani/settings/ani_settings.cpp
+++ b/ani/settings/ani_settings.cpp
@@ -278,14 +278,9 @@
         .uri = "",
         .status = 0,
     };
-    if (asyncCallbackInfo == nullptr) {
-        SETTING_LOG_ERROR("asyncCallbackInfo is null");
-    }
     ThrowExistingError(env, UNSUPPORT_CODE, "");
-    if (asyncCallbackInfo != nullptr) {
-        delete asyncCallbackInfo;
-        asyncCallbackInfo = nullptr;
-    }
+    delete asyncCallbackInfo;
+    asyncCallbackInfo = nullptr;
 }
 
 ani_boolean ani_can_show_floating(ani_env *env)
@@ -299,15 +294,9 @@
         .uri = "",
         .status = 0,
     };
-    if (asyncCallbackInfo == nullptr) {
-        SETTING_LOG_ERROR("asyncCallbackInfo is null");
-        return false;
-    }
     ThrowExistingError(env, UNSUPPORT_CODE, "");
-    if (asyncCallbackInfo != nullptr) {
-        delete asyncCallbackInfo;
-        asyncCallbackInfo = nullptr;
-    }
+    delete asyncCallbackInfo;
+    asyncCallbackInfo = nullptr;
     return true;
 }
 


```

---

## [21/50] ID: CPP_0006 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ani/settings/ani_settings.cpp`
- **Warning:** Function parameter 'tableName' should be passed by const reference.

### Buggy Snippet
```cpp
std::shared_ptr<DataShareHelper> getDataShareHelper(
    ani_env *env, const ani_object context, std::string tableName, AsyncCallbackInfo *asyncCallbackInfo)
{
    std::shared_ptr<OHOS::DataShare::DataShareHelper> dataShareHelper = nullptr;
    int currentUserId = -1;
    OHOS::AccountSA::OsAccountManager::GetOsAccountLocalIdFromProcess(currentUserId);
    int tmpId = 100;
    if (currentUserId > 0) {
        tmpId = currentUserId;
        SETTING_LOG_INFO("userId is %{public}d", tmpId);
    } else if (currentUserId == 0) {
        OHOS::AccountSA::OsAccountManager::GetForegroundOsAccountLocalId(currentUserId);
        tmpId = currentUserId;
        SETTING_LOG_INFO("user0 userId is %{public}d", tmpId);
    } else {
        SETTING_LOG_ERROR("userid is invalid, use id 100 instead");
    }
    std::string strUri = "datashare:///com.ohos.settingsdata.DataAbility";
    std::string strProxyUri = GetProxyUriStr(tableName, tmpId);
    OHOS::Uri proxyUri(strProxyUri);
    SETTING_LOG_INFO("<Ver-11-14> strProxyUri: %{public}s", strProxyUri.c_str());
    auto contextS = OHOS::AbilityRuntime::GetStageModeContext(env, context);
    if (contextS == nullptr) {
        SETTING_LOG_ERROR("get context is error.");
        return dataShareHelper;
    }
    dataShareHelper = OHOS::DataShare::DataShareHelper::Creator(contextS->GetToken(), strProxyUri);
    if (!dataShareHelper) {
        SETTING_LOG_ERROR("dataShareHelper from strProxyUri is null");
        dataShareHelper = OHOS::DataShare::DataShareHelper::Creator(contextS->GetToken(), strUri);
        if (asyncCallbackInfo) {
            asyncCallbackInfo->useSilent = false;
        }
    }
    SETTING_LOG_INFO("g_D_S_H Creator called, valid %{public}d", dataShareHelper != nullptr);
    return dataShareHelper;
}
```

### Patch
```diff
// File: ani/settings/ani_settings.cpp
--- a/ani/settings/ani_settings.cpp
+++ b/ani/settings/ani_settings.cpp
@@ -325,7 +325,7 @@
     return retVal;
 }
 
-bool IsTableNameInvalid(std::string tableName)
+bool IsTableNameInvalid(const std::string& tableName)
 {
     if (tableName != "global" && tableName != "system" && tableName != "secure") {
         return true;
@@ -355,7 +355,7 @@
 }
 
 std::shared_ptr<DataShareHelper> getDataShareHelper(
-    ani_env *env, const ani_object context, std::string tableName, AsyncCallbackInfo *asyncCallbackInfo)
+    ani_env *env, const ani_object context, const std::string& tableName, AsyncCallbackInfo *asyncCallbackInfo)
 {
     std::shared_ptr<OHOS::DataShare::DataShareHelper> dataShareHelper = nullptr;
     int currentUserId = -1;
@@ -419,7 +419,7 @@
     return std::string(utf8Buffer);
 }
 
-std::string GetStageUriStr(std::string tableName, int id, std::string keyStr)
+std::string GetStageUriStr(const std::string& tableName, int id, const std::string& keyStr)
 {
     if (id < USERID_HELPER_NUMBER) {
         id = USERID_HELPER_NUMBER;
@@ -441,7 +441,7 @@
     return retStr;
 }
 
-std::string GetProxyUriStr(std::string tableName, int id)
+std::string GetProxyUriStr(const std::string& tableName, int id)
 {
     if (id < USERID_HELPER_NUMBER) {
         id = USERID_HELPER_NUMBER;


```

---

## [22/50] ID: CPP_0113 | C/C++ (F)
- **Rule ID:** `cppcheck/knownConditionTrueFalse`
- **Result:** `SECONDARY_DEFECT: 4`
- **Target File:** `ohos_ssh/library/src/main/cpp/napi/ssh2_napi.cpp`
- **Warning:** Condition 'ssh2Napi' is always true

### Buggy Snippet
```cpp
napi_value SSH2Napi::SetUser(napi_env env, napi_callback_info info) {
    size_t argc = PARAM_COUNT_2;
    napi_value args[PARAM_COUNT_2] = {nullptr};
    napi_value thisVal = nullptr;
    napi_get_cb_info(env, info, &argc, args, &thisVal, nullptr);
    std::string user;
    NapiUtil::JsValueToString(env, args[INDEX_0], STR_DEFAULT_SIZE, user);
    std::string pass;
    NapiUtil::JsValueToString(env, args[INDEX_1], STR_DEFAULT_SIZE, pass);
    if (user.empty() || pass.empty()) {
        return NapiUtil::SetNapiCallInt32(env, NAPI_FAILED);
    }
    SSH2Napi *ssh2Napi = nullptr;
    napi_unwrap(env, thisVal, (void **)&ssh2Napi);
    if (!ssh2Napi) {
        return NapiUtil::SetNapiCallInt32(env, NAPI_FAILED);
    }
    if (ssh2Napi) {
        ssh2Napi->_user = user;
        ssh2Napi->_pass = pass;
    }
    SetUserPass(user, pass);
    LOGD("SetUser success");
    return NapiUtil::SetNapiCallInt32(env, NAPI_SUCCESS);
}
```

### Patch
```diff
// File: ohos_ssh/library/src/main/cpp/napi/ssh2_napi.cpp
--- a/ohos_ssh/library/src/main/cpp/napi/ssh2_napi.cpp
+++ b/ohos_ssh/library/src/main/cpp/napi/ssh2_napi.cpp
@@ -362,10 +362,8 @@
     if (!ssh2Napi) {
         return NapiUtil::SetNapiCallInt32(env, NAPI_FAILED);
     }
-    if (ssh2Napi) {
-        ssh2Napi->_user = user;
-        ssh2Napi->_pass = pass;
-    }
+    ssh2Napi->_user = user;
+    ssh2Napi->_pass = pass;
     SetUserPass(user, pass);
     LOGD("SetUser success");
     return NapiUtil::SetNapiCallInt32(env, NAPI_SUCCESS);


```

---

## [23/50] ID: CPP_0025 | C/C++ (F)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `SECONDARY_DEFECT: 81`
- **Target File:** `napi/settings/napi_settings.cpp`
- **Warning:** Local variable 'valueType' shadows outer variable

### Buggy Snippet
```cpp
napi_value napi_get_uri(napi_env env, napi_callback_info info)
{
    SETTING_LOG_INFO("uri called");
    // Check the number of the arguments
    size_t argc = ARGS_THREE;
    napi_value args[ARGS_THREE] = {nullptr};
    NAPI_CALL(env, napi_get_cb_info(env, info, &argc, args, nullptr, nullptr));
    if (argc != ARGS_ONE && argc != ARGS_TWO && argc != ARGS_THREE) {
        SETTING_LOG_ERROR(
            "uri %{public}s, wrong number of arguments, expect 1 or 2 or 3 but get %{public}zd",
            __func__,
            argc);
        return wrap_void_to_js(env);
    }

    // Check the value type of the arguments
    napi_valuetype valueType;
    NAPI_CALL(env, napi_typeof(env, args[PARAM0], &valueType));
    NAPI_ASSERT(env, valueType == napi_string, "uri Wrong argument type. String expected.");

    // check call type for stage model
    CallType callType = INVALID_CALL;
    if (argc == ARGS_ONE) {
        callType = STAGE_PROMISE;
    } else if (argc == ARGS_TWO) {
        napi_valuetype valueType;
        NAPI_CALL(env, napi_typeof(env, args[PARAM1], &valueType));
        if (valueType == napi_string) {
            callType = STAGE_PROMISE_SPECIFIC;
        } else {
            callType = STAGE_CALLBACK;
        }
    } else if (argc == ARGS_THREE) {
        callType = STAGE_CALLBACK_SPECIFIC;
    }

    SETTING_LOG_INFO("uri arg count is %{public}zd", argc);
    AsyncCallbackInfo* asyncCallbackInfo = new AsyncCallbackInfo {
        .env = env,
        .asyncWork = nullptr,
        .deferred = nullptr,
        .callbackRef = nullptr,
        .dataAbilityHelper = nullptr,
        .key = "",
        .value = "",
        .uri = "",
        .status = false,
    };
    if (asyncCallbackInfo == nullptr) {
        SETTING_LOG_ERROR("asyncCallbackInfo is null");
        return wrap_void_to_js(env);
    }
    std::string keyStr = unwrap_string_from_js(env, args[PARAM0]);
    // get userId string
    int currentUserId = -1;
    OHOS::AccountSA::OsAccountManager::GetOsAccountLocalIdFromProcess(currentUserId);
    int tmpId = 100;
    if (currentUserId > 0) {
        tmpId = currentUserId;
        SETTING_LOG_INFO("userId is %{public}d", tmpId);
    } else if (currentUserId == 0) {
        OHOS::AccountSA::OsAccountManager::GetForegroundOsAccountLocalId(currentUserId);
        tmpId = currentUserId;
        SETTING_LOG_INFO("user0 userId is %{public}d", tmpId);
    } else {
        SETTING_LOG_ERROR("userid is invalid, use id 100 instead");
    }
    std::string tableName = "";
    if (callType == STAGE_CALLBACK_SPECIFIC) {
        tableName = unwrap_string_from_js(env, args[PARAM2]);
    } else if (callType == STAGE_PROMISE_SPECIFIC) {
        tableName = unwrap_string_from_js(env, args[PARAM1]);
    } else {
        tableName = "global";
    }
    std::string retStr = GetStageUriStr(tableName, tmpId, keyStr);
    asyncCallbackInfo->uri = retStr;
    SETTING_LOG_INFO("uri aft is %{public}s", asyncCallbackInfo->uri.c_str());

    napi_value resource = nullptr;
    NAPI_CALL(env, napi_create_string_utf8(env, "getUri", NAPI_AUTO_LENGTH, &resource));

    if (callType == STAGE_CALLBACK || callType == STAGE_CALLBACK_SPECIFIC) {
        SETTING_LOG_INFO("uri do c_b");
        napi_create_reference(env, args[PARAM1], 1, &asyncCallbackInfo->callbackRef);

        napi_create_async_work(
            env,
            nullptr,
            resource,
            [](napi_env env, void* data) {
                SETTING_LOG_INFO("uri c_b asy execute c_b");
            },
            [](napi_env env, napi_status status, void* data) {
                if (data == nullptr) {
                    SETTING_LOG_INFO("uri c_b asy end data is null");
                    return;
                }
                SETTING_LOG_INFO("uri c_b asy end");
                AsyncCallbackInfo* asyncCallbackInfo = (AsyncCallbackInfo*)data;
                napi_value undefine;
                napi_get_undefined(env, &undefine);
                napi_value callback = nullptr;
                napi_value result = wrap_string_to_js(env, asyncCallbackInfo->uri);
                napi_get_reference_value(env, asyncCallbackInfo->callbackRef, &callback);
                napi_call_function(env, nullptr, callback, 1, &result, &undefine);
                napi_delete_reference(env, asyncCallbackInfo->callbackRef);
                napi_delete_async_work(env, asyncCallbackInfo->asyncWork);
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
                SETTING_LOG_INFO("uri c_b change complete");
            },
            (void*)asyncCallbackInfo,
            &asyncCallbackInfo->asyncWork
        );

        SETTING_LOG_INFO("uri c_b start asy work");
        if (napi_queue_async_work(env, asyncCallbackInfo->asyncWork) != napi_ok) {
            SETTING_LOG_ERROR("napi_queue_async_work error");
            napi_delete_reference(env, asyncCallbackInfo->callbackRef);
            napi_delete_async_work(env, asyncCallbackInfo->asyncWork);
            delete asyncCallbackInfo;
            asyncCallbackInfo = nullptr;
        }
        SETTING_LOG_INFO("uri c_b end asy work");
        return wrap_void_to_js(env);
    } else {
        SETTING_LOG_INFO("uri do p_m");
        napi_value promise;
        napi_deferred deferred;
        if (napi_create_promise(env, &deferred, &promise) != napi_ok) {
            SETTING_LOG_ERROR("napi_create_promise error");
            delete asyncCallbackInfo;
            asyncCallbackInfo = nullptr;
            return nullptr;
        }
        asyncCallbackInfo->deferred = deferred;

        napi_create_async_work(
            env,
            nullptr,
            resource,
            // aysnc executed task
            [](napi_env env, void* data) {
                SETTING_LOG_INFO("uri p_m asy execute c_b");
            },
            // async end called callback+
            [](napi_env env, napi_status status, void* data) {
                SETTING_LOG_INFO("uri p_m asy end");
                AsyncCallbackInfo* asyncCallbackInfo = (AsyncCallbackInfo*)data;
                SETTING_LOG_INFO("uri p_m end get c_b value is %{public}s",
                    asyncCallbackInfo->uri.c_str());
                napi_value result = wrap_string_to_js(env, asyncCallbackInfo->uri);
                napi_resolve_deferred(asyncCallbackInfo->env, asyncCallbackInfo->deferred, result);
                napi_delete_async_work(env, asyncCallbackInfo->asyncWork);
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
            },
            (void*)asyncCallbackInfo,
            &asyncCallbackInfo->asyncWork);
        if (napi_queue_async_work(env, asyncCallbackInfo->asyncWork) != napi_ok) {
            SETTING_LOG_ERROR("napi_queue_async_work error");
            napi_delete_async_work(env, asyncCallbackInfo->asyncWork);
            delete asyncCallbackInfo;
            asyncCallbackInfo = nullptr;
        }
        SETTING_LOG_INFO("uri p_m end asy work");
        return promise;
    }
}
```

### Patch
```diff
// File: napi/settings/napi_settings.cpp
--- a/napi/settings/napi_settings.cpp
+++ b/napi/settings/napi_settings.cpp
@@ -263,7 +263,6 @@
     if (argc == ARGS_ONE) {
         callType = STAGE_PROMISE;
     } else if (argc == ARGS_TWO) {
-        napi_valuetype valueType;
         NAPI_CALL(env, napi_typeof(env, args[PARAM1], &valueType));
         if (valueType == napi_string) {
             callType = STAGE_PROMISE_SPECIFIC;
@@ -1410,7 +1409,7 @@
     if (wrapper != nullptr) {
         asyncCallbackInfo->dataAbilityHelper = wrapper->GetDataAbilityHelper();
     }
-	
+        
     asyncCallbackInfo->key = unwrap_string_from_js(env, args[PARAM1]);
     asyncCallbackInfo->value = unwrap_string_from_js(env, args[PARAM2]);
     SETTING_LOG_INFO("set  input param is : (key %{public}s, value %{public}s)",


```

---

## [24/50] ID: CPP_0320 | C/C++ (F)
- **Rule ID:** `cppcheck/stlIfStrFind`
- **Result:** `LINTER_FAIL`
- **Target File:** `frameworks/js/src/media_library_napi.cpp`
- **Warning:** Inefficient usage of string::find() in condition; string::starts_with() could be faster.

### Buggy Snippet
```cpp
static bool ParseAndSetFileUriArray(const napi_env &env, OHOS::AAFwk::Want &want, const napi_value &value)
{
    uint32_t len = 0;
    CHECK_COND_RET(napi_get_array_length(env, value, &len) == napi_ok, false, "Failed to get array length.");
    if (len > CONFIRM_BOX_ARRAY_MAX_LENGTH) {
        NapiError::ThrowError(env, OHOS_INVALID_PARAM_CODE, "Array size over 100.");
        return false;
    }

    vector<string> srcFileUris;
    for (uint32_t i = 0; i < len; ++i) {
        napi_value element = nullptr;
        CHECK_COND_RET(napi_get_element(env, value, i, &element) == napi_ok, false, "Failed to get array element.");
        if (element == nullptr) {
            NapiError::ThrowError(env, OHOS_INVALID_PARAM_CODE, "Failed to get array element.");
            return false;
        }

        string srcFileUri;
        if (!ParseString(env, element, srcFileUri)) {
            return false;
        }
        NAPI_INFO_LOG("srcFileUri is %{public}s.", srcFileUri.c_str());
        std::string prefix = "https://";
        std::string realUriPath = "";
        if (srcFileUri.find(prefix) == 0) {
            realUriPath = srcFileUri.c_str();
        } else {
            AppFileService::ModuleFileUri::FileUri fileUri(srcFileUri);
            realUriPath = fileUri.ToString();
        }
        NAPI_INFO_LOG("realUriPath is %{public}s.", realUriPath.c_str());

        srcFileUris.emplace_back(realUriPath);
    }

    want.SetParam(CONFIRM_BOX_SRC_FILE_URIS, srcFileUris);

    return true;
}
```

### Patch
```diff
// File: frameworks/js/src/media_library_napi.cpp
--- a/frameworks/js/src/media_library_napi.cpp
+++ b/frameworks/js/src/media_library_napi.cpp
@@ -12531,7 +12531,7 @@
         NAPI_INFO_LOG("srcFileUri is %{public}s.", srcFileUri.c_str());
         std::string prefix = "https://";
         std::string realUriPath = "";
-        if (srcFileUri.find(prefix) == 0) {
+        if (srcFileUri.starts_with(prefix)) {
             realUriPath = srcFileUri.c_str();
         } else {
             AppFileService::ModuleFileUri::FileUri fileUri(srcFileUri);


```

---

## [25/50] ID: CPP_0065 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'msg' should be passed by const reference.

### Buggy Snippet
```cpp
/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "napi_arkts.h"
#include <hilog/log.h>
#include <string>
#include <aki/jsbind.h>
#include "napi_lua.h"
using namespace std;

namespace Ohos_LuaArkts {
napi_env g_env;

std::string TestHelloWorld(std::string msg)
{
    return msg + " too.";
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -22,7 +22,7 @@
 namespace Ohos_LuaArkts {
 napi_env g_env;
 
-std::string TestHelloWorld(std::string msg)
+std::string TestHelloWorld(const std::string& msg)
 {
     return msg + " too.";
 }


```

---

## [26/50] ID: CPP_0168 | C/C++ (F)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `LINTER_FAIL`
- **Target File:** `vap/vap_module/src/main/cpp/render/plugin_render.cpp`
- **Warning:** Local variable 'v1' shadows outer variable

### Buggy Snippet
```cpp
napi_value PluginRender::SetLoop(napi_env env, napi_callback_info info)
{
    LOGD("enter SetLoop");
    NFuncArg funcArg(env, info);
    if (!funcArg.InitArgs(NARG_CNT::ONE, NARG_CNT::TWO)) {
        return nullptr;
    }
    napi_value v1 = funcArg.GetArg(NARG_POS::SECOND);
    NVal nVal(env, v1);
    auto [succ, resData, length] = nVal.ToUTF8String();
    std::string id = resData.get();
    
    LOGD("SetLoop render id:%{public}s", id.c_str());
    std::shared_ptr<PluginRender> render = PluginRender::GetInstance(id);
    if (render) {
        napi_value v1 = funcArg.GetArg(NARG_POS::FIRST);
        NVal nVal(env, v1);
        auto [succ, resData] = nVal.ToInt32();
        LOGD("SetLoop loop: %{public}d", resData);
        if (succ) {
            render->player_->SetLoop(resData);
        } else {
            LOGE("SetLoop cont get val");
        }
    }
    LOGD("end SetLoop");
    return nullptr;
}
```

### Patch
```diff
// File: vap/vap_module/src/main/cpp/render/plugin_render.cpp
--- a/vap/vap_module/src/main/cpp/render/plugin_render.cpp
+++ b/vap/vap_module/src/main/cpp/render/plugin_render.cpp
@@ -314,9 +314,9 @@
     LOGD("SetLoop render id:%{public}s", id.c_str());
     std::shared_ptr<PluginRender> render = PluginRender::GetInstance(id);
     if (render) {
-        napi_value v1 = funcArg.GetArg(NARG_POS::FIRST);
-        NVal nVal(env, v1);
-        auto [succ, resData] = nVal.ToInt32();
+        napi_value loopValue = funcArg.GetArg(NARG_POS::FIRST);
+        NVal loopNVal(env, loopValue);
+        auto [succ, resData] = loopNVal.ToInt32();
         LOGD("SetLoop loop: %{public}d", resData);
         if (succ) {
             render->player_->SetLoop(resData);
@@ -1038,9 +1038,9 @@
             LOGE("the player is running...plz call this func before play.");
             return nullptr;
         }
-        napi_value v1 = funcArg.GetArg(NARG_POS::FIRST);
-        NVal nVal(env, v1);
-        auto [succ, resData, length] = nVal.ToUTF8String();
+        napi_value eventName = funcArg.GetArg(NARG_POS::FIRST);
+        NVal eventNVal(env, eventName);
+        auto [succ, resData, length] = eventNVal.ToUTF8String();
         std::string str = resData.get();
         LOGD("Get Count of argc %{public}zu str:%{public}s", funcArg.GetMaxArgc(), str.c_str());
         if (str != "stateChange" && str != "click") {


```

---

## [27/50] ID: CPP_0079 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'tab' should be passed by const reference.

### Buggy Snippet
```cpp
void T2lSetTableLong(std::string tab, std::string field, int64_t intValue)
{
    auto L = g_L; /* variable in Lua */
    lua_getglobal(L, tab.c_str());
    if (!lua_istable(L, -1)) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0, "ohos_luaarkts", "T2lSetTableLong: %{public}s is not a table",
                     tab.c_str());
        return;
    }
    lua_pushnumber(L, intValue); // 入栈
    int parStackOne = -2;        // 栈从-2开始
    lua_setfield(L, parStackOne, field.c_str());
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -156,7 +156,7 @@
 }
 
 
-void T2lSetTableInt(std::string tab, std::string field, int32_t intValue)
+void T2lSetTableInt(const std::string& tab, std::string field, int32_t intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());
@@ -170,7 +170,7 @@
     lua_setfield(L, parStackOne, field.c_str());
 }
 
-void T2lSetTableLong(std::string tab, std::string field, int64_t intValue)
+void T2lSetTableLong(const std::string& tab, std::string field, int64_t intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());
@@ -184,7 +184,7 @@
     lua_setfield(L, parStackOne, field.c_str());
 }
 
-void T2lSetTableDouble(std::string tab, std::string field, double intValue)
+void T2lSetTableDouble(const std::string& tab, std::string field, double intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());
@@ -198,7 +198,7 @@
     lua_setfield(L, parStackOne, field.c_str());
 }
 
-void T2lSetTableString(std::string tab, std::string field, std::string intValue)
+void T2lSetTableString(const std::string& tab, std::string field, std::string intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());
@@ -212,7 +212,7 @@
     lua_setfield(L, parStackOne, field.c_str());
 }
 
-void T2lSetTableBool(std::string tab, std::string field, bool intValue)
+void T2lSetTableBool(const std::string& tab, std::string field, bool intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());


```

---

## [28/50] ID: CPP_0022 | C/C++ (F)
- **Rule ID:** `cppcheck/knownConditionTrueFalse`
- **Result:** `LINTER_FAIL`
- **Target File:** `napi/settings/napi_settings.cpp`
- **Warning:** Condition 'asyncCallbackInfo!=nullptr' is always true

### Buggy Snippet
```cpp
/**
 * @brief canShowFloating NAPI implementation.
 * @param env the environment that the Node-API call is invoked under
 * @param info the callback info passed into the callback function
 * @return napi_value the return value from NAPI C++ to JS for the module.
 */
napi_value napi_can_show_floating(napi_env env, napi_callback_info info)
{
    const size_t paramOfPromise = PARAM0;
    const size_t paramOfCallback = PARAM1;

    size_t argc = PARAM1;
    napi_value args[PARAM1] = {nullptr};
    NAPI_CALL(env, napi_get_cb_info(env, info, &argc, args, nullptr, nullptr));
    if (argc != paramOfCallback && argc != paramOfPromise) {
        SETTING_LOG_ERROR("%{public}s, wrong number of arguments, expect 0 or 1 but get %{public}zd",
            __func__, argc);
        return wrap_void_to_js(env);
    }

    SETTING_LOG_INFO("n_e_a_m arg count is %{public}zd", argc);
    AsyncCallbackInfo* asyncCallbackInfo = new AsyncCallbackInfo {
        .env = env,
        .asyncWork = nullptr,
        .deferred = nullptr,
        .callbackRef = nullptr,
        .dataAbilityHelper = nullptr,
        .key = "",
        .value = "",
        .uri = "",
        .status = 0,
    };
    if (asyncCallbackInfo == nullptr) {
        SETTING_LOG_ERROR("asyncCallbackInfo is null");
        return wrap_void_to_js(env);
    }
    napi_value resource = nullptr;  
    if (napi_create_string_utf8(env, "enableAirplaneMode", NAPI_AUTO_LENGTH, &resource) != napi_ok) {
        SETTING_LOG_ERROR("napi_create_string_utf8 error");
        if (asyncCallbackInfo != nullptr) {
            delete asyncCallbackInfo;
            asyncCallbackInfo = nullptr;
        }
        return nullptr;
    }
    if (argc == paramOfCallback) {
        SETTING_LOG_INFO("%{public}s, a_C_B.", __func__);

        napi_create_reference(env, args[PARAM0], 1, &asyncCallbackInfo->callbackRef);
        napi_create_async_work(
            env,
            nullptr,
            resource,
            [](napi_env env, void* data) {},
            [](napi_env env, napi_status status, void* data) {
                if (data == nullptr) {
                    SETTING_LOG_INFO("c_b asy end data is null");
                    return;
                }
                AsyncCallbackInfo* asyncCallbackInfo = (AsyncCallbackInfo*)data;

                napi_value callback = nullptr;
                napi_value undefined;
                napi_get_undefined(env, &undefined);

                napi_value result[PARAM2] = {0};

                // create error code
                napi_value error = nullptr;
                napi_create_object(env, &error);
                int unSupportCode = 801;
                napi_value errCode = nullptr;
                napi_create_int32(env, unSupportCode, &errCode);
                napi_set_named_property(env, error, "code", errCode);
                result[0] = error;
                result[1] = wrap_bool_to_js(env, false);

                napi_get_reference_value(env, asyncCallbackInfo->callbackRef, &callback);
                napi_value callResult;
                napi_call_function(env, undefined, callback, PARAM2, result, &callResult);

                napi_delete_reference(env, asyncCallbackInfo->callbackRef);
                napi_delete_async_work(env, asyncCallbackInfo->asyncWork);
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
                SETTING_LOG_INFO("c_b change complete");
            },
            (void*)asyncCallbackInfo,
            &asyncCallbackInfo->asyncWork
        );
        if (napi_queue_async_work(env, asyncCallbackInfo->asyncWork) != napi_ok) {
            SETTING_LOG_ERROR("napi_queue_async_work error");
            if (asyncCallbackInfo != nullptr) {
                napi_delete_reference(env, asyncCallbackInfo->callbackRef);
                napi_delete_async_work(env, asyncCallbackInfo->asyncWork);
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
            }
        }
        return wrap_void_to_js(env);
    } else {
        SETTING_LOG_INFO("%{public}s, promise.", __func__);
        napi_deferred deferred;
        napi_value promise;
        if (napi_create_promise(env, &deferred, &promise) != napi_ok) {
            SETTING_LOG_ERROR("napi_create_promise error");
            if (asyncCallbackInfo != nullptr) {
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
            }
            return wrap_void_to_js(env);
        }
        asyncCallbackInfo->deferred = deferred;

        napi_create_async_work(
            env,
            nullptr,
            resource,
            [](napi_env env, void *data) {},
            [](napi_env env, napi_status status, void *data) {
                SETTING_LOG_INFO("%{public}s, promise complete", __func__);
                AsyncCallbackInfo* asyncCallbackInfo = (AsyncCallbackInfo*)data;

                napi_value result;
                napi_value error = nullptr;
                napi_create_object(env, &error);
                int unSupportCode = 801;
                napi_value errCode = nullptr;
                napi_create_int32(env, unSupportCode, &errCode);
                napi_set_named_property(env, error, "code", errCode);
                result = error;

                napi_reject_deferred(env, asyncCallbackInfo->deferred, result);
                napi_delete_async_work(env, asyncCallbackInfo->asyncWork);
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
            },
            (void *)asyncCallbackInfo,
            &asyncCallbackInfo->asyncWork);
        if (napi_queue_async_work(env, asyncCallbackInfo->asyncWork) != napi_ok) {
            SETTING_LOG_ERROR("napi_queue_async_work error");
            if (asyncCallbackInfo != nullptr) {
                napi_delete_async_work(env, asyncCallbackInfo->asyncWork);
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
            }
        }
        return promise;
    }
}
```

### Patch
```diff
// File: napi/settings/napi_settings.cpp
--- a/napi/settings/napi_settings.cpp
+++ b/napi/settings/napi_settings.cpp
@@ -275,7 +275,7 @@
     }
 
     SETTING_LOG_INFO("uri arg count is %{public}zd", argc);
-    AsyncCallbackInfo* asyncCallbackInfo = new AsyncCallbackInfo {
+    AsyncCallbackInfo* asyncCallbackInfo = new (std::nothrow) AsyncCallbackInfo {
         .env = env,
         .asyncWork = nullptr,
         .deferred = nullptr,
@@ -1410,7 +1410,7 @@
     if (wrapper != nullptr) {
         asyncCallbackInfo->dataAbilityHelper = wrapper->GetDataAbilityHelper();
     }
-	
+        
     asyncCallbackInfo->key = unwrap_string_from_js(env, args[PARAM1]);
     asyncCallbackInfo->value = unwrap_string_from_js(env, args[PARAM2]);
     SETTING_LOG_INFO("set  input param is : (key %{public}s, value %{public}s)",


```

---

## [29/50] ID: CPP_0073 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'strVarInt' should be passed by const reference.

### Buggy Snippet
```cpp
int T2lGetVarInt(string strVarInt)
{
    auto L = g_L; /* variable in Lua */
    lua_getglobal(L, strVarInt.c_str());
    auto result = lua_tointeger(L, -1);

    return result;
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -74,7 +74,7 @@
 }
 
 
-void T2lSetVarInt(string strVarInt, int32_t intValue)
+void T2lSetVarInt(const string& strVarInt, int32_t intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_pushinteger(L, intValue);


```

---

## [30/50] ID: CPP_0275 | C/C++ (F)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `br_proxy/br_proxy_server_manager.c`
- **Warning:** Possible null pointer dereference: nodeInfo

### Buggy Snippet
```cpp
static bool CheckSessionExistByUid(pid_t uid)
{
    if (g_proxyList == NULL) {
        return false;
    }
    if (SoftBusMutexLock(&(g_proxyList->lock)) != SOFTBUS_OK) {
        TRANS_LOGE(TRANS_SVC, "[br_proxy] lock failed");
        return false;
    }
    BrProxyInfo *nodeInfo = NULL;
    LIST_FOR_EACH_ENTRY(nodeInfo, &(g_proxyList->list), BrProxyInfo, node) {
        if (nodeInfo->uid != uid || !nodeInfo->isConnected) {
            continue;
        }
        bool flag = nodeInfo->isConnected;
        (void)SoftBusMutexUnlock(&(g_proxyList->lock));
        return flag;
    }
    (void)SoftBusMutexUnlock(&(g_proxyList->lock));
    return false;
}
```

### Patch
```diff
// File: br_proxy/br_proxy_server_manager.c
--- a/br_proxy/br_proxy_server_manager.c
+++ b/br_proxy/br_proxy_server_manager.c
@@ -2076,6 +2076,9 @@
     }
     BrProxyInfo *nodeInfo = NULL;
     LIST_FOR_EACH_ENTRY(nodeInfo, &(g_proxyList->list), BrProxyInfo, node) {
+        if (nodeInfo == NULL) {
+            continue;
+        }
         if (nodeInfo->uid != uid || !nodeInfo->isConnected) {
             continue;
         }


```

---

## [31/50] ID: CPP_0276 | C/C++ (F)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `br_proxy/br_proxy_server_manager.c`
- **Warning:** Possible null pointer dereference: nodeInfo

### Buggy Snippet
```cpp
static bool IsUidExist(pid_t uid)
{
    if (g_retryList == NULL) {
        TRANS_LOGE(TRANS_SVC, "[br_proxy] Something that couldn't have happened!");
        return false;
    }
    if (SoftBusMutexLock(&(g_retryList->lock)) != SOFTBUS_OK) {
        TRANS_LOGE(TRANS_SVC, "[br_proxy] lock failed");
        return false;
    }
    RetryInfo *nodeInfo = NULL;
    LIST_FOR_EACH_ENTRY(nodeInfo, &(g_retryList->list), RetryInfo, node) {
        if (nodeInfo->uid != uid) {
            continue;
        }
        (void)SoftBusMutexUnlock(&(g_retryList->lock));
        TRANS_LOGI(TRANS_SVC, "[br_proxy] the uid is exist!");
        return true;
    }
    (void)SoftBusMutexUnlock(&(g_retryList->lock));
    return false;
}
```

### Patch
```diff
// File: br_proxy/br_proxy_server_manager.c
--- a/br_proxy/br_proxy_server_manager.c
+++ b/br_proxy/br_proxy_server_manager.c
@@ -2112,6 +2112,9 @@
     }
     RetryInfo *nodeInfo = NULL;
     LIST_FOR_EACH_ENTRY(nodeInfo, &(g_retryList->list), RetryInfo, node) {
+        if (nodeInfo == NULL) {
+            continue;
+        }
         if (nodeInfo->uid != uid) {
             continue;
         }


```

---

## [32/50] ID: CPP_0077 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'strVarBool' should be passed by const reference.

### Buggy Snippet
```cpp
int T2lGetVarBool(string strVarBool)
{
    auto L = g_L; /* variable in Lua */
    lua_getglobal(L, strVarBool.c_str());
    auto result = lua_toboolean(L, -1);

    return result;
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -102,7 +102,7 @@
     lua_setglobal(L, strVarChar.c_str());
 }
 
-void T2lSetVarBool(string strVarBool, bool boolValue)
+void T2lSetVarBool(const string& strVarBool, bool boolValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_pushboolean(L, boolValue);


```

---

## [33/50] ID: CPP_0322 | C/C++ (F)
- **Rule ID:** `cppcheck/identicalInnerCondition`
- **Result:** `SECONDARY_DEFECT: 2`
- **Target File:** `frameworks/js/src/thumbnail_manager.cpp`
- **Warning:** Identical inner 'if' condition is always true.

### Buggy Snippet
```cpp
shared_ptr<ThumbnailManager> ThumbnailManager::GetInstance()
{
    if (instance_ == nullptr) {
        lock_guard<mutex> lock(mutex_);
        if (instance_ == nullptr) {
            instance_ = shared_ptr<ThumbnailManager>(new ThumbnailManager());
        }
    }

    return instance_;
}
```

### Patch
```diff
// File: frameworks/js/src/thumbnail_manager.cpp
--- a/frameworks/js/src/thumbnail_manager.cpp
+++ b/frameworks/js/src/thumbnail_manager.cpp
@@ -172,14 +172,17 @@
 
 shared_ptr<ThumbnailManager> ThumbnailManager::GetInstance()
 {
-    if (instance_ == nullptr) {
+    auto localInstance = instance_;
+    if (localInstance == nullptr) {
         lock_guard<mutex> lock(mutex_);
-        if (instance_ == nullptr) {
+        localInstance = instance_;
+        if (localInstance == nullptr) {
             instance_ = shared_ptr<ThumbnailManager>(new ThumbnailManager());
-        }
-    }
-
-    return instance_;
+            localInstance = instance_;
+        }
+    }
+
+    return localInstance;
 }
 
 void ThumbnailManager::Init()


```

---

## [34/50] ID: CPP_0301 | C/C++ (F)
- **Rule ID:** `cppcheck/redundantAssignment`
- **Result:** `SECONDARY_DEFECT: 5`
- **Target File:** `sdk/transmission/session/src/client_trans_session_callback.c`
- **Warning:** Variable 'session->routeType' is reassigned a value before the old one has been used.

### Buggy Snippet
```cpp
static int32_t FillSessionInfo(SessionInfo *session, const ChannelInfo *channel, uint32_t flag)
{
    session->channelId = channel->channelId;
    session->channelType = (ChannelType)channel->channelType;
    session->routeType = channel->routeType;
    session->enableMultipath = channel->enableMultipath;
    session->peerPid = channel->peerPid;
    session->peerUid = channel->peerUid;
    session->isServer = channel->isServer;
    session->enableStatus = ENABLE_STATUS_SUCCESS;
    session->info.flag = (int32_t)flag;
    session->isEncrypt = channel->isEncrypt;
    session->businessType = channel->businessType;
    session->routeType = channel->routeType;
    session->fileEncrypt = channel->fileEncrypt;
    session->algorithm = channel->algorithm;
    session->crc = channel->crc;
    session->dataConfig = channel->dataConfig;
    session->isAsync = false;
    session->osType = channel->osType;
    session->lifecycle.sessionState = SESSION_STATE_CALLBACK_FINISHED;
    session->isSupportTlv = channel->isSupportTlv;
    session->tokenType = channel->tokenType;
    if (channel->isD2D) {
        session->isD2D = channel->isD2D;
        session->dataLen = channel->dataLen;
        if (channel->dataLen > 0 && channel->dataLen <= EXTRA_DATA_MAX_LEN &&
            memcpy_s(session->extraData, EXTRA_DATA_MAX_LEN, channel->extraData, channel->dataLen) != EOK) {
            TRANS_LOGE(TRANS_SDK, "copy extraData failed");
            return SOFTBUS_MEM_ERR;
        }
        if (channel->isServer &&
            strcpy_s(session->peerPagingAccountId, ACCOUNT_UID_LEN_MAX, channel->pagingAccountId) != EOK) {
            TRANS_LOGE(TRANS_SDK, "copy peerPagingAccountId failed");
            return SOFTBUS_STRCPY_ERR;
        }
        if (strcpy_s(session->info.peerDeviceId, DEVICE_ID_SIZE_MAX, channel->peerDeviceId) != EOK) {
            TRANS_LOGE(TRANS_SDK, "copy peerDeviceId failed");
            return SOFTBUS_STRCPY_ERR;
        }
        return SOFTBUS_OK;
    }
    return FillSessionInfoEx(session, channel);
}
```

### Patch
```diff
// File: sdk/transmission/session/src/client_trans_session_callback.c
--- a/sdk/transmission/session/src/client_trans_session_callback.c
+++ b/sdk/transmission/session/src/client_trans_session_callback.c
@@ -64,7 +64,6 @@
 {
     session->channelId = channel->channelId;
     session->channelType = (ChannelType)channel->channelType;
-    session->routeType = channel->routeType;
     session->enableMultipath = channel->enableMultipath;
     session->peerPid = channel->peerPid;
     session->peerUid = channel->peerUid;


```

---

## [35/50] ID: CPP_0026 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `napi/settings/napi_settings.cpp`
- **Warning:** Function parameter 'errorMessage' should be passed by const reference.

### Buggy Snippet
```cpp
/*
 * Copyright (c) 2022-2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "napi_settings.h"
#include "napi_settings_observer.h"

#include <pthread.h>
#include <unistd.h>

#include "abs_shared_result_set.h"
#include "napi_settings_log.h"
#include "values_bucket.h"
#include "datashare_business_error.h"

#include "napi_base_context.h"
#include "os_account_manager.h"


using namespace OHOS::AppExecFwk;
using namespace OHOS::DataShare;
using namespace OHOS::AccountSA;

namespace OHOS {
namespace Settings {
const std::string SETTINGS_DATA_BASE_URI = "dataability:///com.ohos.settingsdata.DataAbility";
const std::string SETTINGS_DATA_FIELD_KEYWORD = "KEYWORD";
const std::string SETTINGS_DATA_FIELD_VALUE = "VALUE";
const std::string PERMISSION_EXCEPTION = "Permission denied";
const std::string DEFAULT_ANONYMOUS = "******";
const int PERMISSION_EXCEPTION_CODE = 201;
const int QUERY_SUCCESS_CODE = 1;
const int STATUS_ERROR_CODE = -1;
const int PERMISSION_DENIED_CODE = -2;
const int USERID_HELPER_NUMBER = 100;
const int DATA_SHARE_DIED1 = 29189;
const int DATA_SHARE_DIED2 = 32;
std::shared_ptr<OHOS::DataShare::DataShareHelper> globalDataShareHelper = nullptr;
std::mutex helper;

void ThrowExistingError(napi_env env, int errorCode, std::string errorMessage)
{
    napi_value code;
    napi_value message;
    napi_value error;
    napi_create_uint32(env, errorCode, &code);
    napi_create_string_utf8(env, errorMessage.c_str(), NAPI_AUTO_LENGTH, &message);
    napi_create_error(env, code, message, &error);
    napi_throw(env, error);
}
```

### Patch
```diff
// File: napi/settings/napi_settings.cpp
--- a/napi/settings/napi_settings.cpp
+++ b/napi/settings/napi_settings.cpp
@@ -49,7 +49,7 @@
 std::shared_ptr<OHOS::DataShare::DataShareHelper> globalDataShareHelper = nullptr;
 std::mutex helper;
 
-void ThrowExistingError(napi_env env, int errorCode, std::string errorMessage)
+void ThrowExistingError(napi_env env, int errorCode, const std::string& errorMessage)
 {
     napi_value code;
     napi_value message;
@@ -1410,7 +1410,7 @@
     if (wrapper != nullptr) {
         asyncCallbackInfo->dataAbilityHelper = wrapper->GetDataAbilityHelper();
     }
-	
+        
     asyncCallbackInfo->key = unwrap_string_from_js(env, args[PARAM1]);
     asyncCallbackInfo->value = unwrap_string_from_js(env, args[PARAM2]);
     SETTING_LOG_INFO("set  input param is : (key %{public}s, value %{public}s)",


```

---

## [36/50] ID: CPP_0106 | C/C++ (F)
- **Rule ID:** `cppcheck/knownConditionTrueFalse`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_smack/library/src/main/cpp/room.cpp`
- **Warning:** Condition 'data==nullptr' is always false

### Buggy Snippet
```cpp
void room::handleMUCParticipantPresence(MUCRoom * /* room */, const MUCRoomParticipant participant,
    const Presence &presence)
{
    LOGD("handleMUCParticipantPresence Presence is %d of nick: %s, reason: %s,status: %s,"
        "affiliation: %d, role: %d, flag: %d",
        presence.presence(), participant.nick->resource().c_str(), participant.reason.c_str(),
        participant.status.c_str(), participant.affiliation, participant.role, participant.flags);

    if (tsfn_mucp == nullptr) {
        LOGE("smack handleMUCParticipantPresence  %s:  %d", "handleMUCParticipantPresence return  ", __LINE__);
        return;
    }

    std::string nick = participant.nick->resource().c_str(); // 用户昵称
    std::string presenceType = presenceTypeDetect(presence); // 用户状态
    std::string affiliationType = affiliationTypeDetect(participant); // 岗位从属关系
    std::string roleType = roleTypeDetect(participant);
    std::string flagType = flagTypeDetect(participant);
    std::string jsonStr;

    if (flagType == "2") {
        nick = participant.newNick;
    }

    jsonStr.append("{");
    jsonStr.append("\"presenceType\":\"");
    jsonStr.append(presenceType.c_str());
    jsonStr.append("\",");
    jsonStr.append("\"affiliationType\":\"");
    jsonStr.append(affiliationType.c_str());
    jsonStr.append("\",");
    jsonStr.append("\"roleType\":\"");
    jsonStr.append(roleType.c_str());
    jsonStr.append("\",");
    jsonStr.append("\"flagType\":\"");
    jsonStr.append(flagType.c_str());
    jsonStr.append("\"");
    jsonStr.append("}");
    LOGD("handleMUCParticipantPresence ===>>>> %s %s \n", nick.c_str(), flagType.c_str());
    ThreadSafeInfoMUCP *data = &g_threadInfoMUCP;
    if (data == nullptr) {
        LOGE("SMACK_TAG---------> [room.handleMUCParticipantPresence]data is null");
        return;
    }
    data->nike = nick.c_str();
    data->presenceType = jsonStr.c_str();
    napi_acquire_threadsafe_function(tsfn_mucp);
    LOGI("SMACK_TAG--------->: %s:  %d", "handleMUCMessage: ", __LINE__);
    // 调用主线程函数，传入 Data
    napi_call_threadsafe_function(tsfn_mucp, data, napi_tsfn_blocking);
    LOGI("SMACK_TAG--------->: %s:  %d", "handleMUCMessage: ", __LINE__);
}
```

### Patch
```diff
// File: ohos_smack/library/src/main/cpp/room.cpp
--- a/ohos_smack/library/src/main/cpp/room.cpp
+++ b/ohos_smack/library/src/main/cpp/room.cpp
@@ -856,10 +856,6 @@
     jsonStr.append("}");
     LOGD("handleMUCParticipantPresence ===>>>> %s %s \n", nick.c_str(), flagType.c_str());
     ThreadSafeInfoMUCP *data = &g_threadInfoMUCP;
-    if (data == nullptr) {
-        LOGE("SMACK_TAG---------> [room.handleMUCParticipantPresence]data is null");
-        return;
-    }
     data->nike = nick.c_str();
     data->presenceType = jsonStr.c_str();
     napi_acquire_threadsafe_function(tsfn_mucp);
@@ -885,10 +881,6 @@
     LOGI("smack handleMUCMessage  %s:  %d", "handleMUCMessage work  ", __LINE__);
 
     ThreadSafeInfoRoom *data = &g_threadInfoRoom;
-	if (data == nullptr) {
-        LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
-        return;
-    }
     data->id = msg.from().resource().c_str();
     data->msg = body.c_str();
     LOGI("SMACK_TAG--------->: %s:  %d", "handleMUCMessage: ", __LINE__);
@@ -924,10 +916,6 @@
         features, name.c_str(), infoForm->tag()->xml().c_str());
 
     ThreadSafeRoomInfo *data = &g_threadRoomInfo;
-    if (data == nullptr) {
-        LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
-        return;
-    }
     data->roomInfo = infoForm->tag()->xml().c_str();
     NapiJsCallBack(data);
 }
@@ -961,10 +949,6 @@
     LOGD("requestRoomConfig handleMUCConfigForm tag:%s", form.tag()->xml().c_str());
 
     ThreadSafeRoomInfo *data = &g_threadRoomInfo;
-    if (data == nullptr) {
-        LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
-        return;
-    }
     data->roomInfo = form.tag()->xml().c_str();
     NapiJsCallBack(data);
 }
@@ -1026,7 +1010,7 @@
 
 void room::handleMUCConfigList(MUCRoom *room, const MUCListItemList &items, MUCOperation operation)
 {
-	if (room == nullptr) {
+        if (room == nullptr) {
         LOGE("SMACK_TAG---------> [room.handleMUCConfigList]room is null");
         return;
     }


```

---

## [37/50] ID: CPP_0349 | C/C++ (F)
- **Rule ID:** `cppcheck/uninitvar`
- **Result:** `SECONDARY_DEFECT: 4`
- **Target File:** `library/src/main/cpp/napi/http2_utils.h`
- **Warning:** Uninitialized variables: requestTask.errCode, requestTask.buff, requestTask.buffLen

### Buggy Snippet
```cpp
RequestTask ParseDomain(string domain)
{
    size_t pos = domain.find(':');
    RequestTask requestTask;
    if (pos != std::string::npos) {
        std::string host = domain.substr(0, pos);
        std::string port = domain.substr(pos + 1);
        requestTask.host =  host;
        requestTask.port =  port;
    }
    return requestTask;
}
```

### Patch
```diff
// File: library/src/main/cpp/napi/http2_utils.h
--- a/library/src/main/cpp/napi/http2_utils.h
+++ b/library/src/main/cpp/napi/http2_utils.h
@@ -124,6 +124,9 @@
 {
     size_t pos = domain.find(':');
     RequestTask requestTask;
+    requestTask.errCode = 0;
+    requestTask.buff = nullptr;
+    requestTask.buffLen = 0;
     if (pos != std::string::npos) {
         std::string host = domain.substr(0, pos);
         std::string port = domain.substr(pos + 1);


```

---

## [38/50] ID: CPP_0071 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'strVarChar' should be passed by const reference.

### Buggy Snippet
```cpp
void T2lSetVarChar(string strVarChar, const char *charValue)
{
    auto L = g_L; /* variable in Lua */
    lua_pushstring(L, charValue);
    lua_setglobal(L, strVarChar.c_str());
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -95,7 +95,7 @@
     lua_setglobal(L, strVarDouble.c_str());
 }
 
-void T2lSetVarChar(string strVarChar, const char *charValue)
+void T2lSetVarChar(const string& strVarChar, const char *charValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_pushstring(L, charValue);


```

---

## [39/50] ID: CPP_0072 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'strVarBool' should be passed by const reference.

### Buggy Snippet
```cpp
void T2lSetVarBool(string strVarBool, bool boolValue)
{
    auto L = g_L; /* variable in Lua */
    lua_pushboolean(L, boolValue);
    lua_setglobal(L, strVarBool.c_str());
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -102,7 +102,7 @@
     lua_setglobal(L, strVarChar.c_str());
 }
 
-void T2lSetVarBool(string strVarBool, bool boolValue)
+void T2lSetVarBool(const string& strVarBool, bool boolValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_pushboolean(L, boolValue);


```

---

## [40/50] ID: CPP_0059 | C/C++ (F)
- **Rule ID:** `cppcheck/variableScope`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/util/parson.c`
- **Warning:** The scope of the variable 'k' can be reduced.

### Buggy Snippet
```cpp
static JSON_Status json_object_remove_internal(JSON_Object *object, const char *name, parson_bool_t free_value) {
    unsigned long hash = 0;
    parson_bool_t found = PARSON_FALSE;
    size_t cell = 0;
    size_t item_ix = 0;
    size_t last_item_ix = 0;
    size_t i = 0;
    size_t j = 0;
    size_t x = 0;
    size_t k = 0;
    JSON_Value *val = NULL;

    if (object == NULL) {
        return JSONFailure;
    }

    hash = hash_string(name, strlen(name));
    found = PARSON_FALSE;
    cell = json_object_get_cell_ix(object, name, strlen(name), hash, &found);
    if (!found) {
        return JSONFailure;
    }

    item_ix = object->cells[cell];
    if (free_value) {
        val = object->values[item_ix];
        json_value_free(val);
        val = NULL;
    }

    parson_free(object->names[item_ix]);
    last_item_ix = object->count - 1;
    if (item_ix < last_item_ix) {
        object->names[item_ix] = object->names[last_item_ix];
        object->values[item_ix] = object->values[last_item_ix];
        object->cell_ixs[item_ix] = object->cell_ixs[last_item_ix];
        object->hashes[item_ix] = object->hashes[last_item_ix];
        object->cells[object->cell_ixs[item_ix]] = item_ix;
    }
    object->count--;

    i = cell;
    j = i;
    for (x = 0; x < (object->cell_capacity - 1); x++) {
        j = (j + 1) & (object->cell_capacity - 1);
        if (object->cells[j] == OBJECT_INVALID_IX) {
            break;
        }
        k = object->hashes[object->cells[j]] & (object->cell_capacity - 1);
        if ((j > i && (k <= i || k > j))
            || (j < i && (k <= i && k > j))) {
            object->cell_ixs[object->cells[j]] = i;
            object->cells[i] = object->cells[j];
            i = j;
        }
    }
    object->cells[i] = OBJECT_INVALID_IX;
    return JSONSuccess;
}
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/util/parson.c
--- a/ohos_YYEVA/library/src/main/cpp/util/parson.c
+++ b/ohos_YYEVA/library/src/main/cpp/util/parson.c
@@ -620,7 +620,6 @@
     size_t i = 0;
     size_t j = 0;
     size_t x = 0;
-    size_t k = 0;
     JSON_Value *val = NULL;
 
     if (object == NULL) {
@@ -659,7 +658,7 @@
         if (object->cells[j] == OBJECT_INVALID_IX) {
             break;
         }
-        k = object->hashes[object->cells[j]] & (object->cell_capacity - 1);
+        size_t k = object->hashes[object->cells[j]] & (object->cell_capacity - 1);
         if ((j > i && (k <= i || k > j))
             || (j < i && (k <= i && k > j))) {
             object->cell_ixs[object->cells[j]] = i;


```

---

## [41/50] ID: CPP_0223 | C/C++ (F)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `SECONDARY_DEFECT: 6`
- **Target File:** `services/service/src/discovery/discovery_manager.cpp`
- **Warning:** Consider using std::find_if algorithm instead of a raw loop.

### Buggy Snippet
```cpp
void DiscoveryManager::OnDiscoveringResult(const std::string &pkgName, int32_t subscribeId, int32_t result)
{
    LOGI("subscribeId = %{public}d, result = %{public}d.", subscribeId, result);
    int32_t userId = -1;
    std::string callerPkgName = "";
    GetPkgNameAndUserId(pkgName, callerPkgName, userId);
    ProcessInfo processInfo;
    processInfo.userId = userId;
    processInfo.pkgName = callerPkgName;
    if (pkgName.empty() || (listener_ == nullptr)) {
        LOGE("DiscoveryManager::OnDiscoveringResult failed, IDeviceManagerServiceListener is null.");
        return;
    }
    uint16_t externalSubId = DM_INVALID_FLAG_ID;
    {
        std::lock_guard<std::mutex> autoLock(subIdMapLocks_);
        for (auto iter : pkgName2SubIdMap_[pkgName]) {
            if (iter.second == subscribeId) {
                externalSubId = iter.first;
                break;
            }
        }
    }
    if (result == 0) {
        std::lock_guard<std::mutex> autoLock(locks_);
        discoveryContextMap_[pkgName].subscribeId = (uint32_t)externalSubId;
        listener_->OnDiscoverySuccess(processInfo, externalSubId);
        return;
    }
    {
        std::lock_guard<std::mutex> autoLock(locks_);
        if (pkgNameSet_.find(pkgName) != pkgNameSet_.end()) {
            pkgNameSet_.erase(pkgName);
        }
        if (discoveryContextMap_.find(pkgName) != discoveryContextMap_.end()) {
            discoveryContextMap_.erase(pkgName);
            std::lock_guard<std::mutex> lock(timerLocks_);
            if (timer_ != nullptr) {
                timer_->DeleteTimer(pkgName);
            }
        }
    }
    {
        std::lock_guard<std::mutex> capLock(capabilityMapLocks_);
        if (capabilityMap_.find(pkgName) != capabilityMap_.end()) {
            capabilityMap_.erase(pkgName);
        }
    }
    listener_->OnDiscoveryFailed(processInfo, (uint32_t)externalSubId, result);
    softbusListener_->StopRefreshSoftbusLNN(subscribeId);
}
```

### Patch
```diff
// File: services/service/src/discovery/discovery_manager.cpp
--- a/services/service/src/discovery/discovery_manager.cpp
+++ b/services/service/src/discovery/discovery_manager.cpp
@@ -15,6 +15,7 @@
 
 #include "discovery_manager.h"
 
+#include <algorithm>
 #include <dlfcn.h>
 #include "softbus_common.h"
 
@@ -466,11 +467,10 @@
     uint16_t externalSubId = DM_INVALID_FLAG_ID;
     {
         std::lock_guard<std::mutex> autoLock(subIdMapLocks_);
-        for (auto iter : pkgName2SubIdMap_[pkgName]) {
-            if (iter.second == subscribeId) {
-                externalSubId = iter.first;
-                break;
-            }
+        auto it = std::find_if(pkgName2SubIdMap_[pkgName].begin(), pkgName2SubIdMap_[pkgName].end(),
+            [subscribeId](const auto& iter) { return iter.second == subscribeId; });
+        if (it != pkgName2SubIdMap_[pkgName].end()) {
+            externalSubId = it->first;
         }
     }
     if (result == 0) {


```

---

## [42/50] ID: CPP_0219 | C/C++ (F)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `LINTER_FAIL`
- **Target File:** `services/service/src/device_manager_service_listener.cpp`
- **Warning:** Consider using std::find_if algorithm instead of a raw loop.

### Buggy Snippet
```cpp
int32_t DeviceManagerServiceListener::OnServiceInfoOffline(const DmRegisterServiceState &registerServiceState,
    const DmServiceInfo &serviceInfo)
{
    LOGI("OnServiceInfoOffline start.");
    std::shared_ptr<IpcNotifyServiceStateReq> pReq = std::make_shared<IpcNotifyServiceStateReq>();
    std::shared_ptr<IpcRsp> pRsp = std::make_shared<IpcRsp>();

    std::string notifyPkgName = registerServiceState.pkgName;
    pReq->SetDmRegisterServiceState(registerServiceState);
    pReq->SetDmServiceInfo(serviceInfo);
    pReq->SetServiceState(DmServiceState::SERVICE_STATE_OFFLINE);
    std::vector<ProcessInfo> processInfos = ipcServerListener_.GetAllProcessInfo();
    ProcessInfo processInfoTemp;
    for (const auto &item : processInfos) {
        if (item.pkgName == registerServiceState.pkgName && item.userId == registerServiceState.userId) {
            processInfoTemp = item;
            break;
        }
    }
    if (processInfoTemp.pkgName.empty()) {
        LOGI("not register listener");
        return ERR_DM_FAILED;
    }
    pReq->SetPkgName(processInfoTemp.pkgName);
    pReq->SetProcessInfo(processInfoTemp);
    int32_t ret = ipcServerListener_.SendRequest(SERVER_SERVICE_STATE_NOTIFY, pReq, pRsp);
    if (ret != DM_OK) {
        LOGE("OnServiceInfoOffline failed.");
        return ret;
    }
    LOGI("OnServiceInfoOffline success.");
    return DM_OK;
}
```

### Patch
```diff
// File: services/service/src/device_manager_service_listener.cpp
--- a/services/service/src/device_manager_service_listener.cpp
+++ b/services/service/src/device_manager_service_listener.cpp
@@ -13,6 +13,7 @@
  * limitations under the License.
  */
 
+#include <algorithm>
 #include <set>
 #include <sstream>
 #include "cJSON.h"
@@ -1374,19 +1375,17 @@
     pReq->SetDmServiceInfo(serviceInfo);
     pReq->SetServiceState(DmServiceState::SERVICE_STATE_OFFLINE);
     std::vector<ProcessInfo> processInfos = ipcServerListener_.GetAllProcessInfo();
-    ProcessInfo processInfoTemp;
-    for (const auto &item : processInfos) {
-        if (item.pkgName == registerServiceState.pkgName && item.userId == registerServiceState.userId) {
-            processInfoTemp = item;
-            break;
-        }
-    }
-    if (processInfoTemp.pkgName.empty()) {
+    auto it = std::find_if(processInfos.begin(), processInfos.end(),
+                          [&registerServiceState](const auto& item) {
+                              return item.pkgName == registerServiceState.pkgName &&
+                                     item.userId == registerServiceState.userId;
+                          });
+    if (it == processInfos.end()) {
         LOGI("not register listener");
         return ERR_DM_FAILED;
     }
-    pReq->SetPkgName(processInfoTemp.pkgName);
-    pReq->SetProcessInfo(processInfoTemp);
+    pReq->SetPkgName(it->pkgName);
+    pReq->SetProcessInfo(*it);
     int32_t ret = ipcServerListener_.SendRequest(SERVER_SERVICE_STATE_NOTIFY, pReq, pRsp);
     if (ret != DM_OK) {
         LOGE("SERVER_SERVICE_STATE_NOTIFY request failed.");


```

---

## [43/50] ID: CPP_0330 | C/C++ (F)
- **Rule ID:** `cppcheck/redundantAssignment`
- **Result:** `SECONDARY_DEFECT: 5`
- **Target File:** `services/media_backup_extension/src/clone_restore.cpp`
- **Warning:** Variable 'cloneConfigInfo.isValid' is reassigned a value before the old one has been used.

### Buggy Snippet
```cpp
CloneRestoreConfigInfo CloneRestore::GetCurrentDeviceCloneConfigInfo()
{
    CloneRestoreConfigInfo cloneConfigInfo;
    cloneConfigInfo.switchStatus = SettingsDataManager::GetPhotosSyncSwitchStatus();
    if (cloneConfigInfo.switchStatus == SwitchStatus::NONE) {
        int32_t isCloudSpaceSyncSwitchOn = BackupFileUtils::IsCloneCloudSpaceSyncSwitchOn(sceneCode_);
        MEDIA_WARN_LOG("fail to query photo sync switch status, isCloudSpaceSyncSwitchOn:%{public}d",
            isCloudSpaceSyncSwitchOn);
        cloneConfigInfo.switchStatus = (isCloudSpaceSyncSwitchOn == CheckSwitchType::SUCCESS_ON ?
            SwitchStatus::CLOUD : SwitchStatus::NONE);
    }
    bool isSyncSwitchStatusValid = (cloneConfigInfo.switchStatus != SwitchStatus::NONE);
    bool isDeviceIdValid = (cloneConfigInfo.switchStatus == SwitchStatus::HDC ?
        SettingsDataManager::GetHdcDeviceId(cloneConfigInfo.deviceId) : true);
    if (!isDeviceIdValid) {
        MEDIA_ERR_LOG("fail to get deviceId of current device");
        cloneConfigInfo.switchStatus = SwitchStatus::NONE;
        cloneConfigInfo.deviceId = "";
        cloneConfigInfo.isValid = false;
    }
    cloneConfigInfo.isValid = (isSyncSwitchStatusValid && isDeviceIdValid);
    MEDIA_INFO_LOG("GetCurrentDeviceCloneConfigInfo, %{public}s",
        cloneConfigInfo.ToString().c_str());
    return cloneConfigInfo;
}
```

### Patch
```diff
// File: services/media_backup_extension/src/clone_restore.cpp
--- a/services/media_backup_extension/src/clone_restore.cpp
+++ b/services/media_backup_extension/src/clone_restore.cpp
@@ -512,7 +512,6 @@
         MEDIA_ERR_LOG("fail to get deviceId of current device");
         cloneConfigInfo.switchStatus = SwitchStatus::NONE;
         cloneConfigInfo.deviceId = "";
-        cloneConfigInfo.isValid = false;
     }
     cloneConfigInfo.isValid = (isSyncSwitchStatusValid && isDeviceIdValid);
     MEDIA_INFO_LOG("GetCurrentDeviceCloneConfigInfo, %{public}s",


```

---

## [44/50] ID: CPP_0058 | C/C++ (F)
- **Rule ID:** `cppcheck/variableScope`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/util/parson.c`
- **Warning:** The scope of the variable 'cell' can be reduced.

### Buggy Snippet
```cpp
static size_t json_object_get_cell_ix(const JSON_Object *object, const char *key, size_t key_len, unsigned long hash, parson_bool_t *out_found) {
    size_t cell_ix = hash & (object->cell_capacity - 1);
    size_t cell = 0;
    size_t ix = 0;
    unsigned int i = 0;
    unsigned long hash_to_check = 0;
    const char *key_to_check = NULL;
    size_t key_to_check_len = 0;

    *out_found = PARSON_FALSE;

    for (i = 0; i < object->cell_capacity; i++) {
        ix = (cell_ix + i) & (object->cell_capacity - 1);
        cell = object->cells[ix];
        if (cell == OBJECT_INVALID_IX) {
            return ix;
        }
        hash_to_check = object->hashes[cell];
        if (hash != hash_to_check) {
            continue;
        }
        key_to_check = object->names[cell];
        key_to_check_len = strlen(key_to_check);
        if (key_to_check_len == key_len && strncmp(key, key_to_check, key_len) == 0) {
            *out_found = PARSON_TRUE;
            return ix;
        }
    }
    return OBJECT_INVALID_IX;
}
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/util/parson.c
--- a/ohos_YYEVA/library/src/main/cpp/util/parson.c
+++ b/ohos_YYEVA/library/src/main/cpp/util/parson.c
@@ -528,7 +528,6 @@
 
 static size_t json_object_get_cell_ix(const JSON_Object *object, const char *key, size_t key_len, unsigned long hash, parson_bool_t *out_found) {
     size_t cell_ix = hash & (object->cell_capacity - 1);
-    size_t cell = 0;
     size_t ix = 0;
     unsigned int i = 0;
     unsigned long hash_to_check = 0;
@@ -539,7 +538,7 @@
 
     for (i = 0; i < object->cell_capacity; i++) {
         ix = (cell_ix + i) & (object->cell_capacity - 1);
-        cell = object->cells[ix];
+        size_t cell = object->cells[ix];
         if (cell == OBJECT_INVALID_IX) {
             return ix;
         }


```

---

## [45/50] ID: CPP_0127 | C/C++ (F)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `LINTER_FAIL`
- **Target File:** `socketio_tls/library/src/main/cpp/socketio_module_napi.cpp`
- **Warning:** Null pointer dereference: bind

### Buggy Snippet
```cpp
napi_value SocketIOClient::JsConstructor(napi_env env, napi_callback_info info)
{
    napi_value targetObj = nullptr;
    void *data = nullptr;
    size_t argsNum = 0;
    napi_value args[2] = {nullptr};
    napi_get_cb_info(env, info, &argsNum, args, &targetObj, &data);

    SocketIOClient *classBind = new SocketIOClient();
    uintptr_t classId = reinterpret_cast<uintptr_t>(classBind);
    std::string classIdStrTemp = std::to_string(classId);
    classBind->classIdStr = classIdStrTemp;

    napi_value napiClassId;
    napi_create_string_utf8(env, classIdStrTemp.c_str(), classIdStrTemp.length(), &napiClassId);
    napi_set_named_property(env, targetObj, "classId", napiClassId);
    g_clientMap.insert(std::pair<std::string, SocketIOClient *>(classIdStrTemp, classBind));

    napi_wrap(
        env, nullptr, classBind,
        [](napi_env env, void *data, void *hint) {
            SocketIOClient *bind = (SocketIOClient *)data;
            delete bind;
            bind = nullptr;
            g_clientMap.erase(bind->classIdStr);
        },
        nullptr, nullptr);
    return targetObj;
}
```

### Patch
```diff
// File: socketio_tls/library/src/main/cpp/socketio_module_napi.cpp
--- a/socketio_tls/library/src/main/cpp/socketio_module_napi.cpp
+++ b/socketio_tls/library/src/main/cpp/socketio_module_napi.cpp
@@ -1058,10 +1058,12 @@
     
     tsfunc_context->CreateTsFunction(on_event_listener_call_aux, "on", tsfunc_context, CallJsEmit);
 
-    get_socket(classIdStr)
-        ->on(eventName, *tsfunc_context,
-             std::bind(&ClientSocket::on_event_listener_aux, &g_clientSocket, std::placeholders::_1,
-                       std::placeholders::_2, std::placeholders::_3, std::placeholders::_4, std::placeholders::_5));
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->on(eventName, *tsfunc_context,
+                   std::bind(&ClientSocket::on_event_listener_aux, &g_clientSocket, std::placeholders::_1,
+                             std::placeholders::_2, std::placeholders::_3, std::placeholders::_4, std::placeholders::_5));
+    }
     return 0;
 }
 
@@ -1087,10 +1089,12 @@
     
     tsfunc_context->CreateTsFunction(on_event_listener_call_aux, "on_binary", tsfunc_context, CallJsBinary);
 
-    get_socket(classIdStr)
-        ->on(eventName, *tsfunc_context,
-             std::bind(&ClientSocket::on_binary_event_listener_aux, &g_clientSocket, std::placeholders::_1,
-                       std::placeholders::_2, std::placeholders::_3, std::placeholders::_4, std::placeholders::_5));
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->on(eventName, *tsfunc_context,
+                   std::bind(&ClientSocket::on_binary_event_listener_aux, &g_clientSocket, std::placeholders::_1,
+                             std::placeholders::_2, std::placeholders::_3, std::placeholders::_4, std::placeholders::_5));
+    }
     return 0;
 }
 
@@ -1116,10 +1120,12 @@
     
     tsfunc_context->CreateTsFunction(on_event_listener_call_aux, "once", tsfunc_context, CallJsEmit);
 
-    get_socket(classIdStr)
-        ->on(eventName, *tsfunc_context,
-             std::bind(&ClientSocket::once_event_listener_aux, &g_clientSocket, std::placeholders::_1,
-                       std::placeholders::_2, std::placeholders::_3, std::placeholders::_4, std::placeholders::_5));
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->on(eventName, *tsfunc_context,
+                   std::bind(&ClientSocket::once_event_listener_aux, &g_clientSocket, std::placeholders::_1,
+                             std::placeholders::_2, std::placeholders::_3, std::placeholders::_4, std::placeholders::_5));
+    }
     return 0;
 }
 
@@ -1135,7 +1141,10 @@
     char classId[CLASSID_BUF_SIZE] = {0};
     napi_get_value_string_utf8(env, args[1], classId, CLASSID_BUF_SIZE, &charLen);
     std::string classIdStr = classId;
-    get_socket(classIdStr)->off(eventName);
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->off(eventName);
+    }
     return 0;
 }
 
@@ -1148,7 +1157,10 @@
     char classId[CLASSID_BUF_SIZE] = {0};
     napi_get_value_string_utf8(env, args[0], classId, CLASSID_BUF_SIZE, &charLen);
     std::string classIdStr = classId;
-    get_socket(classIdStr)->off_all();
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->off_all();
+    }
     return 0;
 }
 
@@ -1161,7 +1173,10 @@
     char classId[CLASSID_BUF_SIZE] = {0};
     napi_get_value_string_utf8(env, args[0], classId, CLASSID_BUF_SIZE, &charLen);
     std::string classIdStr = classId;
-    get_socket(classIdStr)->close();
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->close();
+    }
     return 0;
 }
 napi_value SocketIOClient::on_error(napi_env env, napi_callback_info info)
@@ -1179,8 +1194,10 @@
     
     NapiCreateThreadsafe(env, on_error_listener_call, CallJsEmit, &g_tsfnOnErrorCall);
 
-    get_socket(classIdStr)
-        ->on_error(std::bind(&ClientSocket::on_error_listener, &g_clientSocket, std::placeholders::_1));
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->on_error(std::bind(&ClientSocket::on_error_listener, &g_clientSocket, std::placeholders::_1));
+    }
     return 0;
 }
 
@@ -1193,7 +1210,10 @@
     char classId[CLASSID_BUF_SIZE] = {0};
     napi_get_value_string_utf8(env, args[0], classId, CLASSID_BUF_SIZE, &charLen);
     std::string classIdStr = classId;
-    get_socket(classIdStr)->off_error();
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->off_error();
+    }
     return 0;
 }
 
@@ -1365,11 +1385,14 @@
     on_emit_tsfn_map[std::string(eventName)].push_back(tsfn_this_emit);
 
     // 通过classId获取socket并发送消息
-    get_socket(classIdStr)->emit(
-        eventName,
-        *messageList,
-        std::bind(&ClientSocket::on_emit_callback, &g_clientSocket, std::placeholders::_1, std::placeholders::_2)
-    );
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->emit(
+            eventName,
+            *messageList,
+            std::bind(&ClientSocket::on_emit_callback, &g_clientSocket, std::placeholders::_1, std::placeholders::_2)
+        );
+    }
 
     delete messageList;
     messageList = nullptr;
@@ -1415,10 +1438,12 @@
     napi_get_value_string_utf8(env, args[ARG_INDEX_4], classId, CLASSID_BUF_SIZE, &charLen);
     std::string classIdStr = classId;
 
-    get_socket(classIdStr)
-        ->emit(eventName, *messageList,
-               std::bind(&ClientSocket::on_emit_callback_binary, &g_clientSocket, std::placeholders::_1,
-                         std::placeholders::_2));
+    sio::socket::ptr socket = get_socket(classIdStr);
+    if (socket) {
+        socket->emit(eventName, *messageList,
+                     std::bind(&ClientSocket::on_emit_callback_binary, &g_clientSocket, std::placeholders::_1,
+                               std::placeholders::_2));
+    }
     delete messageList;
     messageList = nullptr;
     return 0;


```

---

## [46/50] ID: CPP_0080 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'tab' should be passed by const reference.

### Buggy Snippet
```cpp
void T2lSetTableDouble(std::string tab, std::string field, double intValue)
{
    auto L = g_L; /* variable in Lua */
    lua_getglobal(L, tab.c_str());
    if (!lua_istable(L, -1)) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0, "ohos_luaarkts", "T2lSetTableDouble: %{public}s is not a table",
                     tab.c_str());
        return;
    }
    lua_pushnumber(L, intValue); // 入栈
    int parStackOne = -2;        // 栈从-2开始
    lua_setfield(L, parStackOne, field.c_str());
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -156,7 +156,7 @@
 }
 
 
-void T2lSetTableInt(std::string tab, std::string field, int32_t intValue)
+void T2lSetTableInt(const std::string& tab, std::string field, int32_t intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());
@@ -170,7 +170,7 @@
     lua_setfield(L, parStackOne, field.c_str());
 }
 
-void T2lSetTableLong(std::string tab, std::string field, int64_t intValue)
+void T2lSetTableLong(const std::string& tab, std::string field, int64_t intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());
@@ -184,7 +184,7 @@
     lua_setfield(L, parStackOne, field.c_str());
 }
 
-void T2lSetTableDouble(std::string tab, std::string field, double intValue)
+void T2lSetTableDouble(const std::string& tab, std::string field, double intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());
@@ -198,7 +198,7 @@
     lua_setfield(L, parStackOne, field.c_str());
 }
 
-void T2lSetTableString(std::string tab, std::string field, std::string intValue)
+void T2lSetTableString(const std::string& tab, std::string field, std::string intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());
@@ -212,7 +212,7 @@
     lua_setfield(L, parStackOne, field.c_str());
 }
 
-void T2lSetTableBool(std::string tab, std::string field, bool intValue)
+void T2lSetTableBool(const std::string& tab, std::string field, bool intValue)
 {
     auto L = g_L; /* variable in Lua */
     lua_getglobal(L, tab.c_str());


```

---

## [47/50] ID: CPP_0066 | C/C++ (F)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- **Warning:** Function parameter 'sPath' should be passed by const reference.

### Buggy Snippet
```cpp
void InitLuaEnv(std::string sPath)
{
    napi_env env = aki::JSBind::GetScopedEnv();
    g_env = env;
    
    // 1.创建Lua状态
    lua_State *L = luaL_newstate();
    if (L == NULL) {
        return;
    }
    g_L = L;

    luaopen_base(L);
    luaL_openlibs(L);

    luaopen_mLualib(L);

    // 2.加载Lua文件
    int bRet = luaL_loadfile(L, sPath.c_str());
    if (bRet) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0, "ohos_luaarkts", "InitLuaEnv loadfile failed: %{public}s",
                     lua_tostring(L, -1));
        return;
    }

    // 3.运行Lua文件
    bRet = lua_pcall(L, 0, 0, 0);
    if (bRet) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0, "ohos_luaarkts", "InitLuaEnv pcall failed: %{public}s",
                     lua_tostring(L, -1));
        return;
    }

    return;
}
```

### Patch
```diff
// File: ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
--- a/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
+++ b/ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp
@@ -31,7 +31,7 @@
 {
 }
 
-void InitLuaEnv(std::string sPath)
+void InitLuaEnv(const std::string& sPath)
 {
     napi_env env = aki::JSBind::GetScopedEnv();
     g_env = env;


```

---

## [48/50] ID: CPP_0060 | C/C++ (F)
- **Rule ID:** `cppcheck/variableScope`
- **Result:** `LINTER_FAIL`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/util/parson.c`
- **Warning:** The scope of the variable 'c' can be reduced.

### Buggy Snippet
```cpp
static int json_serialize_string(const char *string, size_t len, char *buf) {
    size_t i = 0;
    char c = '\0';
    int written = -1, written_total = 0;
    APPEND_STRING("\"");
    for (i = 0; i < len; i++) {
        c = string[i];
        switch (c) {
            case '\"': APPEND_STRING("\\\""); break;
            case '\\': APPEND_STRING("\\\\"); break;
            case '\b': APPEND_STRING("\\b"); break;
            case '\f': APPEND_STRING("\\f"); break;
            case '\n': APPEND_STRING("\\n"); break;
            case '\r': APPEND_STRING("\\r"); break;
            case '\t': APPEND_STRING("\\t"); break;
            case '\x00': APPEND_STRING("\\u0000"); break;
            case '\x01': APPEND_STRING("\\u0001"); break;
            case '\x02': APPEND_STRING("\\u0002"); break;
            case '\x03': APPEND_STRING("\\u0003"); break;
            case '\x04': APPEND_STRING("\\u0004"); break;
            case '\x05': APPEND_STRING("\\u0005"); break;
            case '\x06': APPEND_STRING("\\u0006"); break;
            case '\x07': APPEND_STRING("\\u0007"); break;
                /* '\x08' duplicate: '\b' */
                /* '\x09' duplicate: '\t' */
                /* '\x0a' duplicate: '\n' */
            case '\x0b': APPEND_STRING("\\u000b"); break;
                /* '\x0c' duplicate: '\f' */
                /* '\x0d' duplicate: '\r' */
            case '\x0e': APPEND_STRING("\\u000e"); break;
            case '\x0f': APPEND_STRING("\\u000f"); break;
            case '\x10': APPEND_STRING("\\u0010"); break;
            case '\x11': APPEND_STRING("\\u0011"); break;
            case '\x12': APPEND_STRING("\\u0012"); break;
            case '\x13': APPEND_STRING("\\u0013"); break;
            case '\x14': APPEND_STRING("\\u0014"); break;
            case '\x15': APPEND_STRING("\\u0015"); break;
            case '\x16': APPEND_STRING("\\u0016"); break;
            case '\x17': APPEND_STRING("\\u0017"); break;
            case '\x18': APPEND_STRING("\\u0018"); break;
            case '\x19': APPEND_STRING("\\u0019"); break;
            case '\x1a': APPEND_STRING("\\u001a"); break;
            case '\x1b': APPEND_STRING("\\u001b"); break;
            case '\x1c': APPEND_STRING("\\u001c"); break;
            case '\x1d': APPEND_STRING("\\u001d"); break;
            case '\x1e': APPEND_STRING("\\u001e"); break;
            case '\x1f': APPEND_STRING("\\u001f"); break;
            case '/':
                if (parson_escape_slashes) {
                    APPEND_STRING("\\/");  /* to make json embeddable in xml\/html */
                } else {
                    APPEND_STRING("/");
                }
                break;
            default:
                if (buf != NULL) {
                    buf[0] = c;
                    buf += 1;
                }
                written_total += 1;
                break;
        }
    }
    APPEND_STRING("\"");
    return written_total;
}
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/util/parson.c
--- a/ohos_YYEVA/library/src/main/cpp/util/parson.c
+++ b/ohos_YYEVA/library/src/main/cpp/util/parson.c
@@ -397,10 +397,9 @@
     return 0;
 #else
     unsigned long hash = 5381;
-    unsigned char c;
     size_t i = 0;
     for (i = 0; i < n; i++) {
-        c = string[i];
+        unsigned char c = string[i];
         if (c == '\0') {
             break;
         }


```

---

## [49/50] ID: CPP_0355 | C/C++ (F)
- **Rule ID:** `cppcheck/uninitvar`
- **Result:** `LINTER_FAIL`
- **Target File:** `ijkplayer/src/main/cpp/ijkplayer/ff_ffplay.c`
- **Warning:** Uninitialized variables: frData.data2, frData.lineSize2

### Buggy Snippet
```cpp
static void record_audio_frame(FFPlayer *ffp, AVFrame *frame)
{
    if (ffp->record_write_data.isInRecord == OHOS_RECORD_STATUS_ON && frame->format == AV_SAMPLE_FMT_FLTP &&
        ffp->record_write_data.recordFramesQueue && frame->linesize[0] > 0) {
        RecordFrameData frData;
        if (frame->channels == DATA_NUM_2 && frame->data[DATA_NUM_1]) {
            frData.data0 = (uint8_t *)av_malloc(frame->linesize[DATA_NUM_0]);
            memcpy(frData.data0, frame->data[DATA_NUM_0], frame->linesize[DATA_NUM_0]);
            frData.lineSize0 = frame->linesize[DATA_NUM_0];
            frData.data1 = (uint8_t *)av_malloc(frame->linesize[DATA_NUM_0]);
            memcpy(frData.data1, frame->data[DATA_NUM_1], frame->linesize[DATA_NUM_0]);
            frData.lineSize1 = frame->linesize[DATA_NUM_0];
        } else {
            frData.data0 = (uint8_t *)av_malloc(frame->linesize[DATA_NUM_0]);
            memcpy(frData.data0, frame->data[DATA_NUM_0], frame->linesize[DATA_NUM_0]);
            frData.lineSize0 = frame->linesize[DATA_NUM_0];
            frData.data1 = (uint8_t *)av_malloc(frame->linesize[DATA_NUM_0]);
            memcpy(frData.data1, frame->data[DATA_NUM_0], frame->linesize[DATA_NUM_0]);
            frData.lineSize1 = frame->linesize[DATA_NUM_0];
        }
        frData.frameType = OHOS_FRAME_TYPE_AUDIO;
        frData.dataNum = FRAME_DATA_NUM_2;
        frData.nb_samples = frame->nb_samples;
        frData.channel_layout = frame->channel_layout;
        frData.channels = frame->channels;
        frData.format = frame->format;
        frData.pts = frame->pts;
        frData.writeFileStatus = DATA_NUM_0;
        int windex = ffp->record_write_data.windex;
        ffp->record_write_data.recordFramesQueue[windex] = frData;
        ffp->record_write_data.windex += DATA_NUM_1;
        ffp->record_write_data.sampleRate = frame->sample_rate;
    }
}
```

### Patch
```diff
// File: ijkplayer/src/main/cpp/ijkplayer/ff_ffplay.c
--- a/ijkplayer/src/main/cpp/ijkplayer/ff_ffplay.c
+++ b/ijkplayer/src/main/cpp/ijkplayer/ff_ffplay.c
@@ -458,15 +458,15 @@
 
     if (!img_info->frame_img_convert_ctx) {
         img_info->frame_img_convert_ctx = sws_getContext(width,
-		    height,
-		    src_frame->format,
-		    dst_width,
-		    dst_height,
-		    AV_PIX_FMT_RGB24,
-		    SWS_BICUBIC,
-		    NULL,
-		    NULL,
-		    NULL);
+                    height,
+                    src_frame->format,
+                    dst_width,
+                    dst_height,
+                    AV_PIX_FMT_RGB24,
+                    SWS_BICUBIC,
+                    NULL,
+                    NULL,
+                    NULL);
 
         if (!img_info->frame_img_convert_ctx) {
             ret = -1;
@@ -482,7 +482,7 @@
             av_log(NULL, AV_LOG_ERROR, "%s avcodec_find_encoder failed\n", __func__);
             goto fail0;
         }
-	    img_info->frame_img_codec_ctx = avcodec_alloc_context3(image_codec);
+            img_info->frame_img_codec_ctx = avcodec_alloc_context3(image_codec);
         if (!img_info->frame_img_codec_ctx) {
             ret = -1;
             av_log(NULL, AV_LOG_ERROR, "%s avcodec_alloc_context3 failed\n", __func__);
@@ -505,7 +505,7 @@
         goto fail0;
     }
     bytes = av_image_get_buffer_size(AV_PIX_FMT_RGB24, dst_width, dst_height, 1);
-	buffer = (uint8_t *) av_malloc(bytes * sizeof(uint8_t));
+        buffer = (uint8_t *) av_malloc(bytes * sizeof(uint8_t));
     if (!buffer) {
         ret = -1;
         av_log(NULL, AV_LOG_ERROR, "%s av_image_get_buffer_size failed\n", __func__);
@@ -632,6 +632,8 @@
             memcpy(frData.data1, frame->data[DATA_NUM_0], frame->linesize[DATA_NUM_0]);
             frData.lineSize1 = frame->linesize[DATA_NUM_0];
         }
+        frData.data2 = NULL;
+        frData.lineSize2 = 0;
         frData.frameType = OHOS_FRAME_TYPE_AUDIO;
         frData.dataNum = FRAME_DATA_NUM_2;
         frData.nb_samples = frame->nb_samples;


```

---

## [50/50] ID: CPP_0273 | C/C++ (F)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `br_proxy/br_proxy_server_manager.c`
- **Warning:** Possible null pointer dereference: nodeInfo

### Buggy Snippet
```cpp
static int32_t GetBrProxyByPid(const char *brMac, const char *uuid, pid_t pid, BrProxyInfo *info)
{
    if (brMac == NULL || uuid == NULL || g_proxyList == NULL || info == NULL) {
        TRANS_LOGE(TRANS_SVC, "[br_proxy] Something that couldn't have happened!");
        return SOFTBUS_INVALID_PARAM;
    }
    if (SoftBusMutexLock(&(g_proxyList->lock)) != SOFTBUS_OK) {
        TRANS_LOGE(TRANS_SVC, "[br_proxy] lock failed");
        return SOFTBUS_LOCK_ERR;
    }
    BrProxyInfo *nodeInfo = NULL;
    LIST_FOR_EACH_ENTRY(nodeInfo, &(g_proxyList->list), BrProxyInfo, node) {
        if (strcmp(nodeInfo->proxyInfo.brMac, brMac) != 0 || strcmp(nodeInfo->proxyInfo.uuid, uuid) != 0 ||
            nodeInfo->pid != pid) {
            continue;
        }
        int32_t ret = memcpy_s(info, sizeof(BrProxyInfo), nodeInfo, sizeof(BrProxyInfo));
        if (ret != EOK) {
            TRANS_LOGE(TRANS_SVC, "[br_proxy] memcpy failed! ret=%{public}d", ret);
            (void)SoftBusMutexUnlock(&(g_proxyList->lock));
            return SOFTBUS_MEM_ERR;
        }
        (void)SoftBusMutexUnlock(&(g_proxyList->lock));
        return SOFTBUS_OK;
    }
    (void)SoftBusMutexUnlock(&(g_proxyList->lock));
    return SOFTBUS_NOT_FIND;
}
```

### Patch
```diff
// File: br_proxy/br_proxy_server_manager.c
--- a/br_proxy/br_proxy_server_manager.c
+++ b/br_proxy/br_proxy_server_manager.c
@@ -1972,6 +1972,9 @@
     }
     BrProxyInfo *nodeInfo = NULL;
     LIST_FOR_EACH_ENTRY(nodeInfo, &(g_proxyList->list), BrProxyInfo, node) {
+        if (nodeInfo == NULL) {
+            continue;
+        }
         if (strcmp(nodeInfo->proxyInfo.brMac, brMac) != 0 || strcmp(nodeInfo->proxyInfo.uuid, uuid) != 0 ||
             nodeInfo->pid != pid) {
             continue;


```

---

