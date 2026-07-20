# Oracle Verdict Audit - False Positives (C/C++)

## [1/50] ID: CPP_0035 | C/C++ (T)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `PASS`
- **Target File:** `napi/settings/open_network_settings/napi_open_network_settings.cpp`
- **Warning:** Function parameter 'message' should be passed by const reference.

### Buggy Snippet
```cpp
napi_value CreateError(napi_env env, int code, std::string message)
{
    napi_value error;
    napi_value tempCode;
    napi_value tempMessage;
    napi_create_string_utf8(env, message.c_str(), NAPI_AUTO_LENGTH, &tempMessage);
    napi_create_uint32(env, code, &tempCode);
    napi_create_error(env, tempCode, tempMessage, &error);
    return error;
}
```

### Patch
```diff
// File: napi/settings/open_network_settings/napi_open_network_settings.cpp
--- a/napi/settings/open_network_settings/napi_open_network_settings.cpp
+++ b/napi/settings/open_network_settings/napi_open_network_settings.cpp
@@ -187,7 +187,7 @@
     return true;
 }
 
-napi_value CreateError(napi_env env, int code, std::string message)
+napi_value CreateError(napi_env env, int code, const std::string &message)
 {
     napi_value error;
     napi_value tempCode;


```

---

## [2/50] ID: CPP_0048 | C/C++ (T)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `PASS`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/mediacodec/capbilities/audio_encoder.cpp`
- **Warning:** Local variable 'ret' shadows outer variable

### Buggy Snippet
```cpp
int32_t AudioEncoder::Config(const SampleInfo &sampleInfo, CodecUserData *codecUserData)
{
    CHECK_AND_RETURN_RET_LOG(encoder_ != nullptr, AVCODEC_SAMPLE_ERR_ERROR, "Encoder is null");
    CHECK_AND_RETURN_RET_LOG(codecUserData != nullptr, AVCODEC_SAMPLE_ERR_ERROR, "Invalid param: codecUserData");

    // Configure audio encoder
    int32_t ret = Configure(sampleInfo);
    CHECK_AND_RETURN_RET_LOG(ret == AVCODEC_SAMPLE_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Configure failed");

    // SetCallback for audio encoder
    ret = SetCallback(codecUserData);
    CHECK_AND_RETURN_RET_LOG(ret == AVCODEC_SAMPLE_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR,
                             "Set callback failed, ret: %{public}d", ret);

    // Prepare audio encoder
    {
        int ret = OH_AudioCodec_Prepare(encoder_);
        CHECK_AND_RETURN_RET_LOG(ret == AV_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Prepare failed, ret: %{public}d", ret);
    }

    return AVCODEC_SAMPLE_ERR_OK;
}
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/mediacodec/capbilities/audio_encoder.cpp
--- a/ohos_YYEVA/library/src/main/cpp/mediacodec/capbilities/audio_encoder.cpp
+++ b/ohos_YYEVA/library/src/main/cpp/mediacodec/capbilities/audio_encoder.cpp
@@ -87,8 +87,8 @@
 
     // Prepare audio encoder
     {
-        int ret = OH_AudioCodec_Prepare(encoder_);
-        CHECK_AND_RETURN_RET_LOG(ret == AV_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Prepare failed, ret: %{public}d", ret);
+        int prepareRet = OH_AudioCodec_Prepare(encoder_);
+        CHECK_AND_RETURN_RET_LOG(prepareRet == AV_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Prepare failed, ret: %{public}d", prepareRet);
     }
 
     return AVCODEC_SAMPLE_ERR_OK;


```

---

## [3/50] ID: CPP_0324 | C/C++ (T)
- **Rule ID:** `cppcheck/stlIfStrFind`
- **Result:** `PASS`
- **Target File:** `services/media_analysis_data_manager/src/dao/medialibrary_analysis_album_operations.cpp`
- **Warning:** Inefficient usage of string::find() in condition; string::starts_with() could be faster.

### Buggy Snippet
```cpp
static string ReorderTagId(string target, const vector<MergeAlbumInfo> &mergeAlbumInfo)
{
    string reordererTagId;
    vector<string> splitResult;
    CHECK_AND_RETURN_RET(!target.empty(), reordererTagId);
    string pattern = ",";
    string strs = target;
    if (static_cast<int32_t>(target.find_last_of(",")) != static_cast<int32_t>(target.size()) - 1) {
        strs += pattern;
    }
    size_t pos = strs.find(pattern);
    while (pos != strs.npos) {
        string groupTag = strs.substr(0, pos);
        strs = strs.substr(pos + 1, strs.size());
        pos = strs.find(pattern);
        if (groupTag.compare(mergeAlbumInfo[0].groupTag) != 0 && groupTag.compare(mergeAlbumInfo[1].groupTag) != 0) {
            splitResult.push_back(groupTag);
        }
    }

    string newTagId = mergeAlbumInfo[0].groupTag + "|" + mergeAlbumInfo[1].groupTag;
    splitResult.push_back(newTagId);
    std::sort(splitResult.begin(), splitResult.end());
    for (auto tagId : splitResult) {
        reordererTagId += (tagId + ",");
    }
    if (static_cast<int32_t>(reordererTagId.find(",")) != static_cast<int32_t>(reordererTagId.size()) - 1) {
        reordererTagId = reordererTagId.substr(0, reordererTagId.size() - 1);
    }
    return reordererTagId;
}
```

### Patch
```diff
// File: services/media_analysis_data_manager/src/dao/medialibrary_analysis_album_operations.cpp
--- a/services/media_analysis_data_manager/src/dao/medialibrary_analysis_album_operations.cpp
+++ b/services/media_analysis_data_manager/src/dao/medialibrary_analysis_album_operations.cpp
@@ -527,7 +527,7 @@
     CHECK_AND_RETURN_RET(!target.empty(), reordererTagId);
     string pattern = ",";
     string strs = target;
-    if (static_cast<int32_t>(target.find_last_of(",")) != static_cast<int32_t>(target.size()) - 1) {
+    if (!target.ends_with(",")) {
         strs += pattern;
     }
     size_t pos = strs.find(pattern);
@@ -546,7 +546,7 @@
     for (auto tagId : splitResult) {
         reordererTagId += (tagId + ",");
     }
-    if (static_cast<int32_t>(reordererTagId.find(",")) != static_cast<int32_t>(reordererTagId.size()) - 1) {
+    if (!reordererTagId.ends_with(",")) {
         reordererTagId = reordererTagId.substr(0, reordererTagId.size() - 1);
     }
     return reordererTagId;


```

---

## [4/50] ID: CPP_0230 | C/C++ (T)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `PASS`
- **Target File:** `adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c`
- **Warning:** Possible null pointer dereference: it

### Buggy Snippet
```cpp
bool SoftbusGattcCheckExistConnectionByAddr(const SoftBusBtAddr *btAddr)
{
    CONN_CHECK_AND_RETURN_RET_LOGE(btAddr != NULL, false, CONN_BLE, "btAddr is null");
    bool isExist = false;
    char macStr[BT_MAC_LEN] = {0};
    if (ConvertBtMacToStr(macStr, BT_MAC_LEN, btAddr->addr, sizeof(btAddr->addr)) != SOFTBUS_OK) {
        CONN_LOGE(CONN_BLE, "convert bt mac to str fail");
        return isExist;
    }
    CONN_CHECK_AND_RETURN_RET_LOGE(g_btAddrs != NULL, false, CONN_BLE, "BtAddrs is null");
    CONN_CHECK_AND_RETURN_RET_LOGE(SoftBusMutexLock(&g_btAddrs->lock) == SOFTBUS_OK,
        false, CONN_BLE, "try to lock fail");
    BleConnMac *it = NULL;
    BleConnMac *next = NULL;
    LIST_FOR_EACH_ENTRY_SAFE(it, next, &g_btAddrs->list, BleConnMac, node) {
        if (StrCmpIgnoreCase((const char *)it->addr, (const char *)macStr) == 0) {
            char anomizeAddress[BT_MAC_LEN] = {0};
            ConvertAnonymizeMacAddress(anomizeAddress, BT_MAC_LEN, macStr, BT_MAC_LEN);
            CONN_LOGE(CONN_BLE, "conn exist, addr=%{public}s", anomizeAddress);
            isExist = true;
            ListDelete(&it->node);
            SoftBusFree(it);
            break;
        }
    }
    (void)SoftBusMutexUnlock(&g_btAddrs->lock);
    return isExist;
}
```

### Patch
```diff
// File: adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
--- a/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
+++ b/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
@@ -291,6 +291,9 @@
     BleConnMac *it = NULL;
     BleConnMac *next = NULL;
     LIST_FOR_EACH_ENTRY_SAFE(it, next, &g_btAddrs->list, BleConnMac, node) {
+        if (it == NULL) {
+            continue;
+        }
         if (StrCmpIgnoreCase((const char *)it->addr, (const char *)macStr) == 0) {
             char anomizeAddress[BT_MAC_LEN] = {0};
             ConvertAnonymizeMacAddress(anomizeAddress, BT_MAC_LEN, macStr, BT_MAC_LEN);


```

---

## [5/50] ID: CPP_0041 | C/C++ (T)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `PASS`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/bean/evaframeall.cpp`
- **Warning:** Function parameter 'datas' should be passed by const reference.

### Buggy Snippet
```cpp
EvaFrameAll::EvaFrameAll(std::list<std::shared_ptr<Datas>> datas) {
//        list<Datas>::iterator it;
//        for (it = datas.begin(); it != datas.end(); ++it) {
//            EvaFrameSet *frameSet = new EvaFrameSet(*it);
//            map.insert(make_pair(frameSet->index, *frameSet));
//        }

    for (std::shared_ptr<Datas> d: datas) {
        auto frameSet = make_shared<EvaFrameSet>(d);
        map[frameSet->index] = frameSet;
    }
}
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/bean/evaframeall.cpp
--- a/ohos_YYEVA/library/src/main/cpp/bean/evaframeall.cpp
+++ b/ohos_YYEVA/library/src/main/cpp/bean/evaframeall.cpp
@@ -5,7 +5,7 @@
 
 }
 
-EvaFrameAll::EvaFrameAll(std::list<std::shared_ptr<Datas>> datas) {
+EvaFrameAll::EvaFrameAll(const std::list<std::shared_ptr<Datas>>& datas) {
 //        list<Datas>::iterator it;
 //        for (it = datas.begin(); it != datas.end(); ++it) {
 //            EvaFrameSet *frameSet = new EvaFrameSet(*it);

--- a/ohos_YYEVA/library/src/main/cpp/bean/evaframeall.h
+++ b/ohos_YYEVA/library/src/main/cpp/bean/evaframeall.h
@@ -12,7 +12,7 @@
     map<int, std::shared_ptr<EvaFrameSet>> map;
     EvaFrameAll();
 
-    EvaFrameAll(std::list<std::shared_ptr<Datas>> datas);
+    EvaFrameAll(const std::list<std::shared_ptr<Datas>>& datas);
 
     ~EvaFrameAll();
 };


```

---

## [6/50] ID: CPP_0184 | C/C++ (T)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `PASS`
- **Target File:** `interfaces/cj/kits/src/device_manager_impl.cpp`
- **Warning:** Local variable 'ret' shadows outer variable

### Buggy Snippet
```cpp
int32_t DeviceManagerFfiImpl::BindTarget(const std::string &deviceId,
    const std::string &bindParam, const bool isMetaType)
{
    if (DeviceManager::GetInstance().CheckNewAPIAccessPermission() != 0) {
        return ERR_NO_PERMISSION;
    }
    int32_t ret = StringCheck(deviceId);
    if (ret != 0) {
        return ret;
    }

    callbackFinished = false;
    if (isMetaType) {
        std::shared_ptr<DmFfiBindTargetCallback> bindTargetCallback = nullptr;
        {
            std::lock_guard<std::mutex> autoLock(g_bindCallbackMapMutex);
            auto iter = g_bindCallbackMap.find(bundleName_);
            if (iter == g_bindCallbackMap.end()) {
                CHECK_SIZE_RETURN(g_bindCallbackMap, DM_ERR_FAILED);
                bindTargetCallback = std::make_shared<DmFfiBindTargetCallback>(bundleName_);
                g_bindCallbackMap[bundleName_] = bindTargetCallback;
            } else {
                bindTargetCallback = iter->second;
            }
        }
        int32_t ret = BindTargetWarpper(deviceId, bindParam, bindTargetCallback);
        if (ret != 0) {
            ret = TransformErrCode(ret);
            LOGE("BindTarget for bundleName %{public}s failed, ret %{public}d", bundleName_.c_str(), ret);
            return ret;
        }
        return WaitForCallbackCv();
    }

    return BindDevice(deviceId, bindParam);
}
```

### Patch
```diff
// File: interfaces/cj/kits/src/device_manager_impl.cpp
--- a/interfaces/cj/kits/src/device_manager_impl.cpp
+++ b/interfaces/cj/kits/src/device_manager_impl.cpp
@@ -455,7 +455,7 @@
                 bindTargetCallback = iter->second;
             }
         }
-        int32_t ret = BindTargetWarpper(deviceId, bindParam, bindTargetCallback);
+        ret = BindTargetWarpper(deviceId, bindParam, bindTargetCallback);
         if (ret != 0) {
             ret = TransformErrCode(ret);
             LOGE("bundleName %{public}s failed, ret %{public}d", bundleName_.c_str(), ret);


```

---

## [7/50] ID: CPP_0247 | C/C++ (T)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `PASS`
- **Target File:** `br_proxy/br_proxy.c`
- **Warning:** Possible null pointer dereference: nodeInfo

### Buggy Snippet
```cpp
static bool IsChannelValid(int32_t channelId)
{
    if (channelId <= 0) {
        return false;
    }
    bool isValid = false;
    if (g_clientList == NULL) {
        TRANS_LOGE(TRANS_SDK, "[br_proxy] not init");
        return isValid;
    }
    if (SoftBusMutexLock(&(g_clientList->lock)) != SOFTBUS_OK) {
        TRANS_LOGE(TRANS_SDK, "[br_proxy] lock failed");
        return isValid;
    }
    ClientBrProxyChannelInfo *nodeInfo = NULL;
    LIST_FOR_EACH_ENTRY(nodeInfo, &(g_clientList->list), ClientBrProxyChannelInfo, node) {
        if (nodeInfo->channelId == channelId) {
            isValid = true;
            break;
        }
    }
    (void)SoftBusMutexUnlock(&(g_clientList->lock));
    return isValid;
}
```

### Patch
```diff
// File: br_proxy/br_proxy.c
--- a/br_proxy/br_proxy.c
+++ b/br_proxy/br_proxy.c
@@ -459,7 +459,7 @@
     }
     ClientBrProxyChannelInfo *nodeInfo = NULL;
     LIST_FOR_EACH_ENTRY(nodeInfo, &(g_clientList->list), ClientBrProxyChannelInfo, node) {
-        if (nodeInfo->channelId == channelId) {
+        if (nodeInfo != NULL && nodeInfo->channelId == channelId) {
             isValid = true;
             break;
         }


```

---

## [8/50] ID: CPP_0090 | C/C++ (T)
- **Rule ID:** `cppcheck/noExplicitConstructor`
- **Result:** `PASS`
- **Target File:** `ohos_pjsip/library/src/main/cpp/common/napi_helper.h`
- **Warning:** Class 'NapiHelper' has a constructor with 1 argument that is not explicit.

### Buggy Snippet
```cpp
//
// Created on 2025/2/21.
//
// Node APIs are not fully supported. To solve the compilation error of the interface cannot be found,
// please include "napi/native_api.h".
#include <string>
#include "napi/native_api.h"

#ifndef OHOS_PJSIP_PROJECT_NAPI_HELPER_H
#define OHOS_PJSIP_PROJECT_NAPI_HELPER_H

class NapiHelper {
public:
    NapiHelper(napi_env env);
    static std::string GetString(napi_env env, napi_value value);
    static napi_value Call(napi_env env, napi_value thisObject, napi_value callback, int argsCount,
                           const napi_value *args);
    static void MaybeRethrowAsCpp(napi_env env_, napi_status status);
    static napi_value GetObjectProperty(napi_env env_, napi_value object, std::string const &key);

private:
    static void MaybeThrowFromStatus(napi_env env, napi_status status, const char *message);

private:
    napi_env env_;
};
```

### Patch
```diff
// File: ohos_pjsip/library/src/main/cpp/common/napi_helper.h
--- a/ohos_pjsip/library/src/main/cpp/common/napi_helper.h
+++ b/ohos_pjsip/library/src/main/cpp/common/napi_helper.h
@@ -11,7 +11,7 @@
 
 class NapiHelper {
 public:
-    NapiHelper(napi_env env);
+    explicit NapiHelper(napi_env env);
     static std::string GetString(napi_env env, napi_value value);
     static napi_value Call(napi_env env, napi_value thisObject, napi_value callback, int argsCount,
                            const napi_value *args);


```

---

## [9/50] ID: CPP_0040 | C/C++ (T)
- **Rule ID:** `cppcheck/noExplicitConstructor`
- **Result:** `PASS`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/bean/evaframeall.h`
- **Warning:** Class 'EvaFrameAll' has a constructor with 1 argument that is not explicit.

### Buggy Snippet
```cpp
//
// Created by zengjiale on 2022/4/19.
//
#pragma once
#include <map>
#include "list"
#include "evaframeset.h"

using namespace std;
class EvaFrameAll {
public:
    map<int, std::shared_ptr<EvaFrameSet>> map;
    EvaFrameAll();

    EvaFrameAll(std::list<std::shared_ptr<Datas>> datas);

    ~EvaFrameAll();
};
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/bean/evaframeall.h
--- a/ohos_YYEVA/library/src/main/cpp/bean/evaframeall.h
+++ b/ohos_YYEVA/library/src/main/cpp/bean/evaframeall.h
@@ -12,7 +12,7 @@
     map<int, std::shared_ptr<EvaFrameSet>> map;
     EvaFrameAll();
 
-    EvaFrameAll(std::list<std::shared_ptr<Datas>> datas);
+    explicit EvaFrameAll(std::list<std::shared_ptr<Datas>> datas);
 
     ~EvaFrameAll();
 };


```

---

## [10/50] ID: CPP_0174 | C/C++ (T)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `PASS`
- **Target File:** `vap/vap_module/src/main/cpp/video_decoder.cpp`
- **Warning:** Local variable 'ret' shadows outer variable

### Buggy Snippet
```cpp
int32_t VideoDecoder::Config(const VAPInfo &info, VDecSignal *signal)
{
    if (decoder_ == nullptr) {
        LOGE("Decoder is null");
        return AV_ERR_UNKNOWN;
    }
    if (signal == nullptr) {
        LOGE("Invalid param: codecUserData");
        return AV_ERR_UNKNOWN;
    }

    // Configure video decoder_
    int32_t ret = ConfigureVideoDecoder(info);
    if (ret != AV_ERR_OK) {
        LOGE("Configure failed");
        return AV_ERR_UNKNOWN;
    }

    // SetCallback for video decoder_
    ret = SetCallback(signal);
    if (ret != AV_ERR_OK) {
        LOGE("Set callback failed, ret: %{public}d", ret);
        return AV_ERR_UNKNOWN;
    }

    // Prepare video decoder_
    {
        int ret = OH_VideoDecoder_Prepare(decoder_);
        if (ret != AV_ERR_OK) {
            LOGE("Prepare failed, ret: %{public}d", ret);
            return AV_ERR_UNKNOWN;
        }
    }

    return AV_ERR_OK;
}
```

### Patch
```diff
// File: vap/vap_module/src/main/cpp/video_decoder.cpp
--- a/vap/vap_module/src/main/cpp/video_decoder.cpp
+++ b/vap/vap_module/src/main/cpp/video_decoder.cpp
@@ -103,12 +103,10 @@
     }
 
     // Prepare video decoder_
-    {
-        int ret = OH_VideoDecoder_Prepare(decoder_);
-        if (ret != AV_ERR_OK) {
-            LOGE("Prepare failed, ret: %{public}d", ret);
-            return AV_ERR_UNKNOWN;
-        }
+    ret = OH_VideoDecoder_Prepare(decoder_);
+    if (ret != AV_ERR_OK) {
+        LOGE("Prepare failed, ret: %{public}d", ret);
+        return AV_ERR_UNKNOWN;
     }
 
     return AV_ERR_OK;


```

---

## [11/50] ID: CPP_0283 | C/C++ (T)
- **Rule ID:** `cppcheck/uninitvar`
- **Result:** `PASS`
- **Target File:** `components/nstackx/fillp/src/public/src/socket_common.c`
- **Warning:** Uninitialized variable: tableIndex

### Buggy Snippet
```cpp
static int SpungeAllocFtSock(struct FtSocketTable *table)
{
    struct FtSocket *sock = FILLP_NULL_PTR;
    int tableIndex;
    if (table == FILLP_NULL_PTR || table->sockPool == FILLP_NULL_PTR) {
        return FILLP_FAILURE;
    }

    sock = (struct FtSocket *)SpungeAlloc(1, sizeof(struct FtSocket), SPUNGE_ALLOC_TYPE_CALLOC);
    if (sock == FILLP_NULL_PTR) {
        return FILLP_FAILURE;
    }

    while (FILLP_TRUE) {
        tableIndex = SYS_ARCH_ATOMIC_READ(&table->used);
        if (tableIndex >= table->size) {
            SpungeFree(sock, SPUNGE_ALLOC_TYPE_CALLOC);
            return FILLP_FAILURE;
        }

        if (CAS((volatile FILLP_ULONG *)&table->sockPool[tableIndex], (volatile FILLP_ULONG)FILLP_NULL_PTR,
            (volatile FILLP_ULONG)sock) == 0) {
            FILLP_USLEEP(1);
        } else {
            break;
        }
    }

    if (SpungeInitSocket(table, tableIndex) != ERR_OK) {
        table->sockPool[tableIndex] = FILLP_NULL_PTR;
        SpungeFree(sock, SPUNGE_ALLOC_TYPE_CALLOC);
        return FILLP_FAILURE;
    }

    SYS_ARCH_ATOMIC_INC(&table->used, 1);
    return FILLP_OK;
}
```

### Patch
```diff
// File: components/nstackx/fillp/src/public/src/socket_common.c
--- a/components/nstackx/fillp/src/public/src/socket_common.c
+++ b/components/nstackx/fillp/src/public/src/socket_common.c
@@ -220,7 +220,7 @@
 static int SpungeAllocFtSock(struct FtSocketTable *table)
 {
     struct FtSocket *sock = FILLP_NULL_PTR;
-    int tableIndex;
+    int tableIndex = 0;
     if (table == FILLP_NULL_PTR || table->sockPool == FILLP_NULL_PTR) {
         return FILLP_FAILURE;
     }


```

---

## [12/50] ID: CPP_0116 | C/C++ (T)
- **Rule ID:** `cppcheck/redundantAssignment`
- **Result:** `PASS`
- **Target File:** `ohos_vlc/library/src/main/cpp/media_wrapper.cpp`
- **Warning:** Variable 'status' is reassigned a value before the old one has been used.

### Buggy Snippet
```cpp
if (status != napi_ok || vlc == nullptr || vlc->instance_ == nullptr) {
        LOGE("unwrap LibVLCWrapper failed");
        return arkTS;
    }
    
    size_t length = 0;
    status = napi_get_value_string_utf8(env, args[1], nullptr, 0, &length);
    std::string buffer(length, '\0');
    status = napi_get_value_string_utf8(env, args[1], &buffer[0], length + 1, &length);
    LOGD("buffer = %s", buffer.c_str());
    
    MediaWrapper* media = new MediaWrapper();
    media->instance_ = libvlc_media_new_location(vlc->instance_, buffer.c_str());
    if (media->instance_ == nullptr) {
        LOGE("libvlc_media_new_location failed");
        delete media;
        return arkTS;
    }
    
    status = napi_wrap(env, arkTS, (void *)media,
                       [](napi_env env, void *finalize_data, void *finalize_hint) {
                           MediaWrapper *media = (MediaWrapper *)finalize_data;
                           libvlc_media_release(media->instance_);
                           if (media->tsfn_ != nullptr) {
                               napi_release_threadsafe_function(media->tsfn_, napi_tsfn_abort);
                           }
                           delete media;
                       },
                       nullptr, nullptr);
    if (status != napi_ok) {
        delete media;
    }
    LOGI("MediaConstructor success");
    return arkTS;
}
```

### Patch
```diff
// File: ohos_vlc/library/src/main/cpp/media_wrapper.cpp
--- a/ohos_vlc/library/src/main/cpp/media_wrapper.cpp
+++ b/ohos_vlc/library/src/main/cpp/media_wrapper.cpp
@@ -33,7 +33,7 @@
     }
     
     size_t length = 0;
-    status = napi_get_value_string_utf8(env, args[1], nullptr, 0, &length);
+    napi_get_value_string_utf8(env, args[1], nullptr, 0, &length);
     std::string buffer(length, '\0');
     status = napi_get_value_string_utf8(env, args[1], &buffer[0], length + 1, &length);
     LOGD("buffer = %s", buffer.c_str());


```

---

## [13/50] ID: CPP_0209 | C/C++ (T)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `PASS`
- **Target File:** `services/implementation/src/devicestate/dm_device_state_manager.cpp`
- **Warning:** Consider using std::find_if algorithm instead of a raw loop.

### Buggy Snippet
```cpp
std::string DmDeviceStateManager::GetUdidByNetWorkId(std::string networkId)
{
    LOGI("networkId %{public}s", GetAnonyString(networkId).c_str());
    {
#if !(defined(__LITEOS_M__) || defined(LITE_DEVICE))
        std::lock_guard<ffrt::mutex> mutexLock(remoteDeviceInfosMutex_);
#else
        std::lock_guard<std::mutex> mutexLock(remoteDeviceInfosMutex_);
#endif
        for (auto &iter : stateDeviceInfos_) {
            if (networkId == iter.second.networkId) {
                return iter.first;
            }
        }
    }
    LOGI("Not find udid by networkid in stateDeviceInfos.");
    return "";
}
```

### Patch
```diff
// File: services/implementation/src/devicestate/dm_device_state_manager.cpp
--- a/services/implementation/src/devicestate/dm_device_state_manager.cpp
+++ b/services/implementation/src/devicestate/dm_device_state_manager.cpp
@@ -15,6 +15,7 @@
 
 #include "dm_device_state_manager.h"
 
+#include <algorithm>
 #include <pthread.h>
 
 #include "dm_anonymous.h"
@@ -676,10 +677,12 @@
 #else
         std::lock_guard<std::mutex> mutexLock(remoteDeviceInfosMutex_);
 #endif
-        for (auto &iter : stateDeviceInfos_) {
-            if (networkId == iter.second.networkId) {
-                return iter.first;
-            }
+        auto iter = std::find_if(stateDeviceInfos_.begin(), stateDeviceInfos_.end(),
+                                 [&networkId](const auto &item) {
+                                     return networkId == item.second.networkId;
+                                 });
+        if (iter != stateDeviceInfos_.end()) {
+            return iter->first;
         }
     }
     LOGI("Not find udid by networkid in stateDeviceInfos.");


```

---

## [14/50] ID: CPP_0112 | C/C++ (T)
- **Rule ID:** `cppcheck/uninitvar`
- **Result:** `PASS`
- **Target File:** `ohos_smack/library/src/main/cpp/room.cpp`
- **Warning:** Uninitialized variable: k

### Buggy Snippet
```cpp
const int ODD_NUMBER = 1;
const int EXPECT_NUMBER = 2;

// 解析配置字符串并生成配置映射
static std::map<std::string, std::string> parseConfigString(const std::string& config)
{
    std::map<std::string, std::string> map;
    std::string str = config.c_str();

    char* p1 = new char[str.size() + 1];
    std::strcpy(p1, str.c_str());
    int len = strlen(p1);
    char *p2;
    char *p3;
    int pos = 1;

    while ((len > 0) && (p2 = strtok(p1, ",")) != nullptr) {
        p1 += strlen(p2) + 1;
        len -= strlen(p2) + 1;

        char *k;
        char *v;
        while ((p3 = strtok(p2, ":")) != nullptr) {
            p2 = nullptr;
            if (pos % EXPECT_NUMBER == ODD_NUMBER) {
                k = p3;
            } else {
                v = p3;
            }
            pos++;
        }
        if (k && v) {
            map[k] = v;
        }
    }
    return map;
}
```

### Patch
```diff
// File: ohos_smack/library/src/main/cpp/room.cpp
--- a/ohos_smack/library/src/main/cpp/room.cpp
+++ b/ohos_smack/library/src/main/cpp/room.cpp
@@ -375,8 +375,8 @@
         p1 += strlen(p2) + 1;
         len -= strlen(p2) + 1;
 
-        char *k;
-        char *v;
+        char *k = nullptr;
+        char *v = nullptr;
         while ((p3 = strtok(p2, ":")) != nullptr) {
             p2 = nullptr;
             if (pos % EXPECT_NUMBER == ODD_NUMBER) {
@@ -885,7 +885,7 @@
     LOGI("smack handleMUCMessage  %s:  %d", "handleMUCMessage work  ", __LINE__);
 
     ThreadSafeInfoRoom *data = &g_threadInfoRoom;
-	if (data == nullptr) {
+        if (data == nullptr) {
         LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
         return;
     }
@@ -1026,7 +1026,7 @@
 
 void room::handleMUCConfigList(MUCRoom *room, const MUCListItemList &items, MUCOperation operation)
 {
-	if (room == nullptr) {
+        if (room == nullptr) {
         LOGE("SMACK_TAG---------> [room.handleMUCConfigList]room is null");
         return;
     }


```

---

## [15/50] ID: CPP_0043 | C/C++ (T)
- **Rule ID:** `cppcheck/noExplicitConstructor`
- **Result:** `PASS`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.h`
- **Warning:** Class 'EvaSrcMap' has a constructor with 1 argument that is not explicit.

### Buggy Snippet
```cpp
//
// Created by zengjiale on 2022/4/19.
//
#pragma once
#include "map"
#include "string"
#include "list"
#include "evasrc.h"
#include "effect.h"

using namespace std;
class EvaSrcMap {
public:
    map<string, shared_ptr<EvaSrc>> map;
    EvaSrcMap();
    EvaSrcMap(list<shared_ptr<Effect>> effects);

    ~EvaSrcMap();
};
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.h
--- a/ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.h
+++ b/ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.h
@@ -13,7 +13,7 @@
 public:
     map<string, shared_ptr<EvaSrc>> map;
     EvaSrcMap();
-    EvaSrcMap(list<shared_ptr<Effect>> effects);
+    explicit EvaSrcMap(list<shared_ptr<Effect>> effects);
 
     ~EvaSrcMap();
 };


```

---

## [16/50] ID: CPP_0356 | C/C++ (T)
- **Rule ID:** `cppcheck/noExplicitConstructor`
- **Result:** `PASS`
- **Target File:** `ijkplayer/src/main/cpp/proxy/ijkplayer_napi_proxy.h`
- **Warning:** Class 'IJKPlayerNapiProxy' has a constructor with 1 argument that is not explicit.

### Buggy Snippet
```cpp
#endif

class IJKPlayerNapiProxy {

  public:
    IJKPlayerNapiProxy(std::string &id) : id_(id){};
    void message_loop_callback(void (*pe)(int what, int arg1, int arg2, char *obj, std::string id));
    void IjkMediaPlayer_native_setup(void *weak_this, void *native_window);
    void IjkMediaPlayer_native_setup_audio();
    void IjkMediaPlayer_setDataSource(char *url);
    void IjkMediaPlayer_setOption(int category, char *name, char *value);
    void IjkMediaPlayer_setOptionLong(int category, char *name, int64_t value);
    void IjkMediaPlayer_prepareAsync();
    void IjkMediaPlayer_start();
    void IjkMediaPlayer_stop();
    void IjkMediaPlayer_pause();
    void IjkMediaPlayer_seekTo(int64_t msec);
    bool IjkMediaPlayer_isPlaying();
    int IjkMediaPlayer_getCurrentPosition();
    int IjkMediaPlayer_getDuration();
    void IjkMediaPlayer_release();
    void IjkMediaPlayer_reset();
    void IjkMediaPlayer_setVolume(float leftVolume, float rightVolume);
    void IjkMediaPlayer_native_setLogLevel(int32_t level);
    void ijkMediaPlayer_setPropertyFloat(int id, float value);
    float ijkMediaPlayer_getPropertyFloat(int id, float default_value);
    void ijkMediaPlayer_setPropertyLong(int id, long value);
    long ijkMediaPlayer_getPropertyLong(int id, long default_value);
    int IjkMediaPlayer_getAudioSessionId();
    void IjkMediaPlayer_setLoopCount(int loop_count);
    int IjkMediaPlayer_getLoopCount();
    char *IjkMediaPlayer_getVideoCodecInfo();
    char *IjkMediaPlayer_getAudioCodecInfo();
    void ijkMediaPlayer_setStreamSelected(int stream, bool selected);
    HashMap IjkMediaPlayer_getMediaMeta();
    void IjkMediaPlayer_native_openlog();
    IjkMediaPlayer *set_media_player(std::string id, IjkMediaPlayer *mp);
    IjkMediaPlayer *get_media_player(std::string id);
    void delete_media_player(std::string id);
    
    int IjkMediaPlayer_startRecord(const char *recordFilePath);
    int IjkMediaPlayer_stopRecord();
    int IjkMediaPlayer_isRecord();
    int IjkMediaPlayer_getCurrentFrame(const char *saveFilePath);
    int IjkMediaPlayer_setRecordDefaultFrameRate(const int frameRate, const bool isPriority);
  public:
    std::string id_;
    void *GLOBAL_NATIVE_WINDOW = nullptr;
    bool IJKMP_GLOABL_INIT = false;
    typedef struct player_fields_t {
        pthread_mutex_t mutex;
    } player_fields_t;
    player_fields_t g_clazz;
};
```

### Patch
```diff
// File: ijkplayer/src/main/cpp/proxy/ijkplayer_napi_proxy.h
--- a/ijkplayer/src/main/cpp/proxy/ijkplayer_napi_proxy.h
+++ b/ijkplayer/src/main/cpp/proxy/ijkplayer_napi_proxy.h
@@ -32,7 +32,7 @@
 class IJKPlayerNapiProxy {
 
   public:
-    IJKPlayerNapiProxy(std::string &id) : id_(id){};
+    explicit IJKPlayerNapiProxy(std::string &id) : id_(id){};
     void message_loop_callback(void (*pe)(int what, int arg1, int arg2, char *obj, std::string id));
     void IjkMediaPlayer_native_setup(void *weak_this, void *native_window);
     void IjkMediaPlayer_native_setup_audio();


```

---

## [17/50] ID: CPP_0164 | C/C++ (T)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `PASS`
- **Target File:** `unrar/library/src/main/cpp/unrar.cpp`
- **Warning:** Local variable 'code' shadows outer variable

### Buggy Snippet
```cpp
static napi_value RarFile_Extract(napi_env env, napi_callback_info info) {
    wchar_t nameW[NM];
    struct RAROpenArchiveDataEx data {};
    memset(nameW, 0, sizeof(char) * NM);
    size_t requireArgc = 3;
    size_t argc = 3;
    napi_value args[3] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    char buf[NM];
    size_t size = NM;
    napi_get_value_string_utf8(env, args[0], buf, size, &size);
    char *paths = buf;
    CgetWC(nameW, paths);
    LOG(" buf = OpenResult1 paths: %{public}s ", paths);

    /* char *test;
    const size_t cSize = NM;
    wcstombs(test, nameW, cSize);*/

    char dest[1024];
    size_t sized = 1024;
    napi_get_value_string_utf8(env, args[1], dest, sized, &sized);
    char *dests = dest;
    LOG(" buf = OpenResult1 dests: %{public}s ", dests);
    wchar_t destPath[NM];
    memset(destPath, 0, sizeof(wchar_t) * NM);
    CgetWC(destPath, dests);

    double mode = RAR_OM_EXTRACT;
    data.ArcNameW = nameW;

    data.OpenMode = (unsigned int)mode;

    HANDLE handle = RAROpenArchiveEx(&data);
    if (handle == nullptr || data.OpenResult) {
        if (handle) {
            RARCloseArchive(handle);
        }
        char err_str[128];
        napi_throw_error(env, err_str, "RarException");
        return 0;
    }
    char passwordss[NM];
    size_t sizes = NM;

    if (napi_ok == napi_get_value_string_utf8(env, args[2], passwordss, sizes, &sizes)) {
        char *passwords = passwordss;
        RARSetPassword(handle, passwords); //190512
        LOG(" buf = OpenResult4 password: %{public}s ", passwordss);
    } else {
        RARSetCallback(handle, nullptr, (LPARAM) nullptr);
    }
    char *results = "";
    struct RARHeaderDataEx header {};
    bool tag;
    tag = true;

    if (napi_ok == napi_get_value_string_utf8(env, args[2], passwordss, sizes, &sizes)) {
        if (RARReadHeaderEx(handle, &header)) {
            results = "密码错误 ";
            tag = false;
        } else {
            int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
            if (code != 0) {
                results = header.FileName;
                tag = false;
            }
            while (!RARReadHeaderEx(handle, &header)) {
                int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
                if (code != 0) {
                    results = header.FileName;
                    tag = false;
                }
            }
        }

    } else {
        while (!RARReadHeaderEx(handle, &header)) {
            int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
            if (code != 0) {
                results = header.FileName;
                tag = false;
            }
        }
    }

    if (handle) {
        RARCloseArchive(handle);
    }
    string success = "解压成功";
    napi_value result;
    if (tag) {
        napi_create_string_utf8(env, success.c_str(), success.length(), &result);
    } else {
        string ss = results;
        string fail = ss + "文件解压失败";
        napi_create_string_utf8(env, fail.c_str(), fail.length(), &result);
    }

    return result;
}
```

### Patch
```diff
// File: unrar/library/src/main/cpp/unrar.cpp
--- a/unrar/library/src/main/cpp/unrar.cpp
+++ b/unrar/library/src/main/cpp/unrar.cpp
@@ -117,14 +117,14 @@
             results = "密码错误 ";
             tag = false;
         } else {
-            int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
-            if (code != 0) {
+            int processCode = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
+            if (processCode != 0) {
                 results = header.FileName;
                 tag = false;
             }
             while (!RARReadHeaderEx(handle, &header)) {
-                int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
-                if (code != 0) {
+                int loopCode = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
+                if (loopCode != 0) {
                     results = header.FileName;
                     tag = false;
                 }
@@ -137,8 +137,8 @@
                 tag2 = false;
                 break;
             }
-            int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
-            if (code != 0) {
+            int processCode = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
+            if (processCode != 0) {
                 results = header.FileName;
                 tag = false;
             }
@@ -348,14 +348,14 @@
             results = "密码错误 ";
             tag = false;
         } else {
-            int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
-            if (code != 0) {
+            int processCode = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
+            if (processCode != 0) {
                 results = header.FileName;
                 tag = false;
             }
             while (!RARReadHeaderEx(handle, &header)) {
-                int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
-                if (code != 0) {
+                int loopCode = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
+                if (loopCode != 0) {
                     results = header.FileName;
                     tag = false;
                 }
@@ -364,8 +364,8 @@
 
     } else {
         while (!RARReadHeaderEx(handle, &header)) {
-            int code = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
-            if (code != 0) {
+            int processCode = RARProcessFileW(handle, RAR_EXTRACT, destPath, NULL);
+            if (processCode != 0) {
                 results = header.FileName;
                 tag = false;
             }


```

---

## [18/50] ID: CPP_0248 | C/C++ (T)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `PASS`
- **Target File:** `br_proxy/br_proxy.c`
- **Warning:** Possible null pointer dereference: nodeInfo

### Buggy Snippet
```cpp
void BrProxyServiceDeathNotify(void)
{
    TRANS_LOGW(TRANS_SDK, "[br_proxy] server die!");
    if (g_clientList == NULL) {
        TRANS_LOGE(TRANS_SDK, "[br_proxy] not init");
        return;
    }
 
    if (SoftBusMutexLock(&(g_clientList->lock)) != SOFTBUS_OK) {
        TRANS_LOGE(TRANS_SDK, "[br_proxy] lock failed");
        return;
    }
    ClientBrProxyChannelInfo *nodeInfo = NULL;
    LIST_FOR_EACH_ENTRY(nodeInfo, &(g_clientList->list), ClientBrProxyChannelInfo, node) {
        if (nodeInfo->enableStateChange && nodeInfo->listener.onChannelStatusChanged != NULL) {
            TRANS_LOGI(TRANS_SDK, "[br_proxy] server died! channelId=%{public}d", nodeInfo->channelId);
            nodeInfo->listener.onChannelStatusChanged(nodeInfo->channelId, CHANNEL_EXCEPTION_SOFTWARE_FAILED);
        }
    }
    (void)SoftBusMutexUnlock(&(g_clientList->lock));
}
```

### Patch
```diff
// File: br_proxy/br_proxy.c
--- a/br_proxy/br_proxy.c
+++ b/br_proxy/br_proxy.c
@@ -798,6 +798,9 @@
     }
     ClientBrProxyChannelInfo *nodeInfo = NULL;
     LIST_FOR_EACH_ENTRY(nodeInfo, &(g_clientList->list), ClientBrProxyChannelInfo, node) {
+        if (nodeInfo == NULL) {
+            continue;
+        }
         if (nodeInfo->enableStateChange && nodeInfo->listener.onChannelStatusChanged != NULL) {
             TRANS_LOGI(TRANS_SDK, "[br_proxy] server died! channelId=%{public}d", nodeInfo->channelId);
             nodeInfo->listener.onChannelStatusChanged(nodeInfo->channelId, CHANNEL_EXCEPTION_SOFTWARE_FAILED);


```

---

## [19/50] ID: CPP_0126 | C/C++ (T)
- **Rule ID:** `cppcheck/functionStatic`
- **Result:** `PASS`
- **Target File:** `socketio_tls/library/src/main/cpp/socketio_module_napi.cpp`
- **Warning:** Technically the member function 'ClientSocket::OnOpen' can be static (but you may consider moving to unnamed namespace).

### Buggy Snippet
```cpp
class ClientSocket {
public:
    ClientSocket() noexcept {}

    void OnOpen()
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, "LOG_TAG", "SOCKETIO_TAG_NAPI------> OnOpen 连接成功");
            
        napi_acquire_threadsafe_function(g_tsfnOnOpenCall);
        // 调用主线程函数，传入 Data
        napi_call_threadsafe_function(g_tsfnOnOpenCall, nullptr, napi_tsfn_blocking);
    }

    void OnFail()
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> OnFail ");
            
        napi_acquire_threadsafe_function(g_tsfnFailCall);
        // 调用主线程函数，传入 Data
        napi_call_threadsafe_function(g_tsfnFailCall, nullptr, napi_tsfn_blocking);
    }

    void OnReconnecting()
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> OnReconnecting ");
            
        napi_acquire_threadsafe_function(g_tsfnReconnectingCall);
        // 调用主线程函数，传入 Data
        napi_call_threadsafe_function(g_tsfnReconnectingCall, nullptr, napi_tsfn_blocking);
    }

    // 待回传unsigned两个参数
    void OnReconnect(unsigned, unsigned)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> OnReconnect ");
            
        napi_acquire_threadsafe_function(g_tsfnReconnectCall);
        // 调用主线程函数，传入 Data
        napi_call_threadsafe_function(g_tsfnReconnectCall, nullptr, napi_tsfn_blocking);
    }

    void on_close(sio::client::close_reason const &reason)
    {
        std::string reasonString = "";
        if (reason == sio::client::close_reason_normal) {
            reasonString = "close_reason_normal";
        } else if (reason == sio::client::close_reason_drop) {
            reasonString = "close_reason_drop";
        }
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> on_close ");
        
        std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
        if (localThreadSafeInfo == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_close]localThreadSafeInfo is null");
            return;
        }
        localThreadSafeInfo->result = reasonString;
        napi_acquire_threadsafe_function(g_tsfnCloseCall);
        napi_call_threadsafe_function(g_tsfnCloseCall, localThreadSafeInfo.release(), napi_tsfn_blocking);
    }

    void on_socket_open(std::string const &nsp)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------>0 on_socket_open %{public}s",
                     nsp.c_str());
        
        std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
        if (localThreadSafeInfo == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_socket_open]localThreadSafeInfo is null");
            return;
        }
        localThreadSafeInfo->result = nsp;
        napi_acquire_threadsafe_function(g_tsfnOnSocketioOpenCall);
        napi_call_threadsafe_function(g_tsfnOnSocketioOpenCall, localThreadSafeInfo.release(), napi_tsfn_blocking);
    }

    void on_socket_close(std::string const &nsp)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> on_socket_close ");
        std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
        if (localThreadSafeInfo == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_socket_close]localThreadSafeInfo is null");
            return;
        }
        localThreadSafeInfo->result = nsp;
        napi_acquire_threadsafe_function(g_tsfnOnCloseCall);
        napi_call_threadsafe_function(g_tsfnOnCloseCall, localThreadSafeInfo.release(), napi_tsfn_blocking);
    }

    void on_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                               sio::message::ptr const &message, bool needAck, sio::message::list &ack_message)
    {
        g_isOnce = false;
        handler_event_listener_aux(context, name, message, needAck,
            ack_message);
    }
    
    void on_binary_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                               sio::message::ptr const &message, bool needAck, sio::message::list &ack_message)
    {
        g_isOnce = false;
        handler_binary_event_listener_aux(context, name, message, needAck,
            ack_message);
    }

    void once_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                                 sio::message::ptr const &message, bool needAck, sio::message::list &ack_message)
    {
        g_isOnce = true;
        handler_event_listener_aux(context, name, message, needAck,
            ack_message);
    }

    void on_error_listener(sio::message::ptr const &message)
    {
        std::string error_string = "on error";
        
        std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
        if (localThreadSafeInfo == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_error_listener]localThreadSafeInfo is null");
            return;
        }
        localThreadSafeInfo->result = error_string;
        napi_acquire_threadsafe_function(g_tsfnOnErrorCall);
        napi_call_threadsafe_function(g_tsfnOnErrorCall, localThreadSafeInfo.release(), napi_tsfn_blocking);
    }
    
    std::string handler_message_json(sio::message::list const &list)
    {
        std::string str;
        if (list.at(0)->get_flag() == sio::message::flag_object) {
            std::map<std::string, sio::message::ptr> messageMap = list.at(0)->get_map();
            for (auto it : messageMap) {
                if (messageMap.begin()->first != it.first) {
                    str += std::string(",");
                }
                str += std::string("\"") + it.first.c_str() + "\":" + get_message_value(it.second);
            }
        } else {
            str += std::string("\"") + "message" + "\":" + get_message_value(list.at(0));
        }
        return str;
    }

    void on_emit_callback(std::string const &ack_name, sio::message::list const &list)
    {
        OH_LOG_Print(LOG_APP,   LOG_INFO,   LOG_DOMAIN,   LOG_TAG, "SOCKETIO_TAG------> 0 on_emit_callback -------");
        napi_ref on_emit_listener_call_ref = on_emit_listener_call_ref_map[ack_name.c_str()];
        if (on_emit_listener_call_ref == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "on_emit_listener_call_ref is null");
            return;
        }
        std::string message_json = std::string("{");
        if (list.size() > 0) {
            message_json += handler_message_json(list);
        }
        message_json += "}";
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> 1 on_emit_callback %{public}s",
                     message_json.c_str());

        auto it = on_emit_tsfn_map.find(ack_name);
        if (it == on_emit_tsfn_map.end() || it->second.empty()) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "TSFN queue empty for event %{public}s",
                         ack_name.c_str());
            return;
        }
        napi_threadsafe_function tsfn = it->second.front();
        it->second.pop_front();
        if (it->second.empty()) {
            on_emit_tsfn_map.erase(it);
        }

        std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
        if (localThreadSafeInfo == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_emit_callback]localThreadSafeInfo is null");
            return;
        }
        localThreadSafeInfo->result = message_json;
        napi_acquire_threadsafe_function(tsfn);
        napi_call_threadsafe_function(tsfn, localThreadSafeInfo.release(), napi_tsfn_blocking);
        napi_release_threadsafe_function(tsfn, napi_tsfn_release);
    }

    void on_emit_callback_binary(std::string const &ack_name, sio::message::list const &list)
    {
        napi_ref on_emit_listener_call_ref = on_emit_listener_call_ref_map[ack_name.c_str()];
        if (on_emit_listener_call_ref == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "on_emit_listener_call_ref is null");
            return;
        }

        if (list.size() > 1) {
            std::unique_ptr<BinaryInfo> localBinaryInfo = std::make_unique<BinaryInfo>();
            if (localBinaryInfo == nullptr) {
                OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[event_listener]g_threadSafeInfo is null");
                return;
            }
            if (list.at(0)->get_flag() == sio::message::flag_integer) {
                localBinaryInfo->code = list.at(0)->get_int();
            }
            if (list.at(1)->get_flag() == sio::message::flag_binary) {
                auto binary_str = *list.at(1)->get_binary();
                localBinaryInfo->result = binary_str;
            }
            napi_acquire_threadsafe_function(g_tsfnEmitBinaryCall);
            napi_call_threadsafe_function(g_tsfnEmitBinaryCall, localBinaryInfo.release(), napi_tsfn_blocking);
        }
    }
};
```

### Patch
```diff
// File: socketio_tls/library/src/main/cpp/socketio_module_napi.cpp
--- a/socketio_tls/library/src/main/cpp/socketio_module_napi.cpp
+++ b/socketio_tls/library/src/main/cpp/socketio_module_napi.cpp
@@ -205,7 +205,7 @@
 public:
     ClientSocket() noexcept {}
 
-    void OnOpen()
+    static void OnOpen()
     {
         OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, "LOG_TAG", "SOCKETIO_TAG_NAPI------> OnOpen 连接成功");
             


```

---

## [20/50] ID: CPP_0357 | C/C++ (T)
- **Rule ID:** `cppcheck/noExplicitConstructor`
- **Result:** `PASS`
- **Target File:** `ijkplayer/src/main/cpp/napi/ijkplayer_napi.h`
- **Warning:** Class 'IJKPlayerNapi' has a constructor with 1 argument that is not explicit.

### Buggy Snippet
```cpp
/*
 * Copyright (C) 2022 Huawei Device Co., Ltd.
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

#ifndef ijkplayer_ijkplayer_napi.h_H
#define ijkplayer_ijkplayer_napi .h_H
#include <string>
#include <unordered_map>
#include <ace/xcomponent/native_interface_xcomponent.h>
#include <napi/native_api.h>
#include "../proxy/ijkplayer_napi_proxy.h"
#include "../utils/napi/napi_utils.h"
#include <uv.h>

class IJKPlayerNapi {

  public:
    IJKPlayerNapi(std::string &id);
    static IJKPlayerNapi *getInstance(std::string &id);
    static napi_value setDataSource(napi_env env, napi_callback_info info);
    static napi_value setOption(napi_env env, napi_callback_info info);
    static napi_value setOptionLong(napi_env env, napi_callback_info info);
    static napi_value setVolume(napi_env env, napi_callback_info info);
    static napi_value prepareAsync(napi_env env, napi_callback_info info);
    static napi_value start(napi_env env, napi_callback_info info);
    static napi_value stop(napi_env env, napi_callback_info info);
    static napi_value pause(napi_env env, napi_callback_info info);
    static napi_value reset(napi_env env, napi_callback_info info);
    static napi_value release(napi_env env, napi_callback_info info);
    static napi_value seekTo(napi_env env, napi_callback_info info);
    static napi_value isPlaying(napi_env env, napi_callback_info info);
    static napi_value getDuration(napi_env env, napi_callback_info info);
    static napi_value getCurrentPosition(napi_env env, napi_callback_info info);
    static napi_value setMessageListener(napi_env env, napi_callback_info info);
    static napi_value setPropertyFloat(napi_env env, napi_callback_info info);
    static napi_value getPropertyFloat(napi_env env, napi_callback_info info);
    static napi_value setPropertyLong(napi_env env, napi_callback_info info);
    static napi_value getPropertyLong(napi_env env, napi_callback_info info);
    static napi_value getAudioSessionId(napi_env env, napi_callback_info info);
    static napi_value setLoopCount(napi_env env, napi_callback_info info);
    static napi_value getLoopCount(napi_env env, napi_callback_info info);
    static napi_value getVideoCodecInfo(napi_env env, napi_callback_info info);
    static napi_value getAudioCodecInfo(napi_env env, napi_callback_info info);
    static napi_value setStreamSelected(napi_env env, napi_callback_info info);
    static napi_value getMediaMeta(napi_env env, napi_callback_info info);
    static napi_value nativeOpenlog(napi_env env, napi_callback_info info);
    static napi_value native_setup(napi_env env, napi_callback_info info);
    static napi_value native_setup_audio(napi_env env, napi_callback_info info);
    static napi_value JsConstructor(napi_env env, napi_callback_info info);
    static napi_value startRecord(napi_env env, napi_callback_info info);
    static napi_value stopRecord(napi_env env, napi_callback_info info);
    static napi_value isRecord(napi_env env, napi_callback_info info);
    static napi_value getCurrentFrame(napi_env env, napi_callback_info info);
    static napi_value stopAsync(napi_env env, napi_callback_info info);
    static napi_value releaseAsync(napi_env env, napi_callback_info info);
    static napi_value setRecordDefaultFrameRate(napi_env env, napi_callback_info info);
    
    ////////////////////////XComponent////////////////////////////
    static OH_NativeXComponent_Callback *getNXComponentCallback();
    void setNativeXComponent(OH_NativeXComponent *component);
    void onSurfaceCreated(OH_NativeXComponent *component, void *window);
    void onSurfaceChanged(OH_NativeXComponent *component, void *window);
    void onSurfaceDestroyed(OH_NativeXComponent *component, void *window);
    void dispatchTouchEvent(OH_NativeXComponent *component, void *window);
    static std::string getXComponentId(napi_env env, napi_callback_info info);
    void setXComponentAndNativeWindow(std::string &id, OH_NativeXComponent *component, void *window);
    OH_NativeXComponent *getXComponent(std::string &id);
    void *getNativeWindow(std::string &id);
    napi_value Export(napi_env env, napi_value exports);

  public:
    IJKPlayerNapiProxy *ijkPlayerNapiProxy_;
    static std::unordered_map<std::string, IJKPlayerNapi *> ijkPlayerNapi_;
    std::unordered_map<std::string, OH_NativeXComponent *> nativeXComponentMap_;
    std::unordered_map<std::string, void *> nativeWindowMap_;
    static OH_NativeXComponent_Callback callback_;
    OH_NativeXComponent *component_;
    std::string id_;
    uint64_t width_ = 0;
    uint64_t height_ = 0;
    OH_NativeXComponent_TouchEvent touchEvent_;
    static bool gIsVideo;
    napi_env envMessage_;
    napi_ref callBackRefMessage_;
};
```

### Patch
```diff
// File: ijkplayer/src/main/cpp/napi/ijkplayer_napi.h
--- a/ijkplayer/src/main/cpp/napi/ijkplayer_napi.h
+++ b/ijkplayer/src/main/cpp/napi/ijkplayer_napi.h
@@ -26,7 +26,7 @@
 class IJKPlayerNapi {
 
   public:
-    IJKPlayerNapi(std::string &id);
+    explicit IJKPlayerNapi(std::string &id);
     static IJKPlayerNapi *getInstance(std::string &id);
     static napi_value setDataSource(napi_env env, napi_callback_info info);
     static napi_value setOption(napi_env env, napi_callback_info info);


```

---

## [21/50] ID: CPP_0237 | C/C++ (T)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `PASS`
- **Target File:** `adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c`
- **Warning:** Possible null pointer dereference: it

### Buggy Snippet
```cpp
static void FindCallbackByUdidAndSetHandle(
    SoftBusBtUuid *serviceUuid, SoftBusGattsCallback *callback, int32_t srvcHandle)
{
    CONN_CHECK_AND_RETURN_LOGE(SoftBusMutexLock(&g_softBusGattsManager.lock) == SOFTBUS_OK,
        CONN_BLE, "lock fail, srvcHandle=%{public}d", srvcHandle);
    ServerService *it = NULL;
    LIST_FOR_EACH_ENTRY(it, &g_softBusGattsManager.services, ServerService, node) {
        if (it->serviceUuid.uuidLen == serviceUuid->uuidLen &&
            memcmp(it->serviceUuid.uuid, serviceUuid->uuid, it->serviceUuid.uuidLen) == 0) {
            *callback = it->callback;
            it->handle = srvcHandle;
            break;
        }
    }
    (void)SoftBusMutexUnlock(&g_softBusGattsManager.lock);
}
```

### Patch
```diff
// File: adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c
--- a/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c
+++ b/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c
@@ -734,7 +734,7 @@
         CONN_BLE, "lock fail, srvcHandle=%{public}d", srvcHandle);
     ServerService *it = NULL;
     LIST_FOR_EACH_ENTRY(it, &g_softBusGattsManager.services, ServerService, node) {
-        if (it->serviceUuid.uuidLen == serviceUuid->uuidLen &&
+        if (it != NULL && it->serviceUuid.uuidLen == serviceUuid->uuidLen &&
             memcmp(it->serviceUuid.uuid, serviceUuid->uuid, it->serviceUuid.uuidLen) == 0) {
             *callback = it->callback;
             it->handle = srvcHandle;


```

---

## [22/50] ID: CPP_0291 | C/C++ (T)
- **Rule ID:** `cppcheck/redundantAssignment`
- **Result:** `PASS`
- **Target File:** `core/bus_center/service/src/bus_center_event.c`
- **Warning:** Variable 'i' is reassigned a value before the old one has been used.

### Buggy Snippet
```cpp
static void NotifyEvent(const LnnEventBasicInfo *info)
{
    LnnEventHandlerItem *item = NULL;
    uint32_t i = 0;

    if (SoftBusMutexLock(&g_eventCtrl.lock) != 0) {
        LNN_LOGE(LNN_EVENT, "lock failed in notify event");
        return;
    }
    uint32_t count = g_eventCtrl.regCnt[info->event];

    if (count == 0) {
        (void)SoftBusMutexUnlock(&g_eventCtrl.lock);
        LNN_LOGE(LNN_EVENT, "count is 0");
        return;
    }
    
    LnnEventHandler *handlesArray = (LnnEventHandler *)SoftBusCalloc(sizeof(LnnEventHandlerItem) * count);
    if (handlesArray == NULL) {
        LNN_LOGE(LNN_EVENT, "malloc failed");
        (void)SoftBusMutexUnlock(&g_eventCtrl.lock);
        return;
    }
    LIST_FOR_EACH_ENTRY(item, &g_eventCtrl.handlers[info->event], LnnEventHandlerItem, node) {
        handlesArray[i] = item->handler;
        i++;
    }
    (void)SoftBusMutexUnlock(&g_eventCtrl.lock);

    /* process handles out of lock */
    for (i = 0; i < count; i++) {
        if (handlesArray[i] != NULL) {
            handlesArray[i](info);
        }
    }
    SoftBusFree(handlesArray);
}
```

### Patch
```diff
// File: core/bus_center/service/src/bus_center_event.c
--- a/core/bus_center/service/src/bus_center_event.c
+++ b/core/bus_center/service/src/bus_center_event.c
@@ -442,9 +442,9 @@
     (void)SoftBusMutexUnlock(&g_eventCtrl.lock);
 
     /* process handles out of lock */
-    for (i = 0; i < count; i++) {
-        if (handlesArray[i] != NULL) {
-            handlesArray[i](info);
+    for (uint32_t j = 0; j < count; j++) {
+        if (handlesArray[j] != NULL) {
+            handlesArray[j](info);
         }
     }
     SoftBusFree(handlesArray);


```

---

## [23/50] ID: CPP_0117 | C/C++ (T)
- **Rule ID:** `cppcheck/redundantAssignment`
- **Result:** `PASS`
- **Target File:** `ohos_vlc/library/src/main/cpp/napi_init.cpp`
- **Warning:** Variable 'status' is reassigned a value before the old one has been used.

### Buggy Snippet
```cpp
/*
# Copyright (c) 2025 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
*/

#include "napi/native_api.h"
#include "libvlc_wrapper.h"
#include "media_player_wrapper.h"
#include "media_wrapper.h"
#include <ace/xcomponent/native_interface_xcomponent.h>
#include "xcomponent_manager.h"
#include "ohos_log.h"
#include "dialog_wrapper.h"

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    LibVLCWrapper::Export(env, exports);
    MediaPlayerWrapper::Export(env, exports);
    MediaWrapper::Export(env, exports);
    DialogWrapper::Export(env, exports);

    napi_status status;
    napi_value xComponentInstance = nullptr;
    OH_NativeXComponent *nativeXComponent = nullptr;
    status = napi_get_named_property(env, exports, OH_NATIVE_XCOMPONENT_OBJ, &xComponentInstance);
    status = napi_unwrap(env, xComponentInstance, reinterpret_cast<void**>(&nativeXComponent));
    if (status != napi_ok) {
        return exports;
    }

    char idStr[OH_XCOMPONENT_ID_LEN_MAX + 1] = {};
    uint64_t idSize = OH_XCOMPONENT_ID_LEN_MAX + 1;
    uint32_t ret = 0;
    ret = OH_NativeXComponent_GetXComponentId(nativeXComponent, idStr, &idSize);
    if (ret != OH_NATIVEXCOMPONENT_RESULT_SUCCESS) {
        return exports;
    }

    LOGD("SetVideoOut id = %s", idStr);
    std::string strId = std::string(idStr);
    xMgr.AddNativeXcomponent(strId, nativeXComponent);
    xMgr.RegisterCallback(strId);
    return exports;
}
```

### Patch
```diff
// File: ohos_vlc/library/src/main/cpp/napi_init.cpp
--- a/ohos_vlc/library/src/main/cpp/napi_init.cpp
+++ b/ohos_vlc/library/src/main/cpp/napi_init.cpp
@@ -34,6 +34,9 @@
     napi_value xComponentInstance = nullptr;
     OH_NativeXComponent *nativeXComponent = nullptr;
     status = napi_get_named_property(env, exports, OH_NATIVE_XCOMPONENT_OBJ, &xComponentInstance);
+    if (status != napi_ok) {
+        return exports;
+    }
     status = napi_unwrap(env, xComponentInstance, reinterpret_cast<void**>(&nativeXComponent));
     if (status != napi_ok) {
         return exports;


```

---

## [24/50] ID: CPP_0344 | C/C++ (T)
- **Rule ID:** `cppcheck/functionStatic`
- **Result:** `PASS`
- **Target File:** `NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp`
- **Warning:** Technically the member function 'ParallelBucketSort::ParallelSortBucket' can be static (but you may consider moving to unnamed namespace).

### Buggy Snippet
```cpp
// 并行桶排序（使用多线程）
class ParallelBucketSort {
private:
    // 并行排序单个桶
    void ParallelSortBucket(vector<int> &bucket) { std::sort(bucket.begin(), bucket.end()); }

public:
    void Sort(vector<int> &arr)
    {
        int n = arr.size();
        if (n <= 1) {
            return;
        }
        // 确定桶数量（根据CPU核心数优化）
        int bucketCount = min(n, static_cast<int>(thread::hardware_concurrency()) * 4);
        bucketCount = max(bucketCount, 4); // 至少4个桶
        // 找到最小值和最大值
        int minVal = *min_element(arr.begin(), arr.end());
        int maxVal = *max_element(arr.begin(), arr.end());
        if (minVal == maxVal) {
            return;
        }
        // 创建桶
        vector<vector<int>> buckets(bucketCount);
        // 分配元素到桶中
        double range = 1.0;
        if (bucketCount != 0) {
            range = static_cast<double>(maxVal - minVal + 1) / bucketCount;
        }
        for (int val : arr) {
            int bucketIndex = 0;
            if (range != 0) {
                bucketIndex = (val - minVal) / range;
                bucketIndex = min(bucketIndex, bucketCount - 1);
                buckets[bucketIndex].push_back(val);
            }
        }
        // 并行排序每个桶
        vector<future<void>> futures;
        for (int i = 0; i < bucketCount; i++) {
            if (!buckets[i].empty()) {
                futures.push_back(
                    async(launch::async, [&buckets, i]() { std::sort(buckets[i].begin(), buckets[i].end()); }));
            }
        }
        // 等待所有桶排序完成
        for (auto &f : futures) {
            f.wait();
        }
        // 合并结果
        int index = 0;
        for (int i = 0; i < bucketCount; i++) {
            for (int val : buckets[i]) {
                arr[index++] = val;
            }
        }
        return;
    }
};
```

### Patch
```diff
// File: NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
--- a/NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
+++ b/NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
@@ -1213,7 +1213,7 @@
 class ParallelBucketSort {
 private:
     // 并行排序单个桶
-    void ParallelSortBucket(vector<int> &bucket) { std::sort(bucket.begin(), bucket.end()); }
+    static void ParallelSortBucket(vector<int> &bucket) { std::sort(bucket.begin(), bucket.end()); }
 
 public:
     void Sort(vector<int> &arr)


```

---

## [25/50] ID: CPP_0296 | C/C++ (T)
- **Rule ID:** `cppcheck/noExplicitConstructor`
- **Result:** `PASS`
- **Target File:** `core/connection/wifi_direct_cpp/event/wifi_direct_event_dispatcher.h`
- **Warning:** Struct 'ProcessorTerminate' has a constructor with 1 argument that is not explicit.

### Buggy Snippet
```cpp
struct ProcessorTerminate : public std::exception {
    ProcessorTerminate(ProcessorTerminateReason reason = ProcessorTerminateReason::SUCCESS) : reason_(reason) {}
    ProcessorTerminateReason reason_;
};
```

### Patch
```diff
// File: core/connection/wifi_direct_cpp/event/wifi_direct_event_dispatcher.h
--- a/core/connection/wifi_direct_cpp/event/wifi_direct_event_dispatcher.h
+++ b/core/connection/wifi_direct_cpp/event/wifi_direct_event_dispatcher.h
@@ -53,7 +53,7 @@
 };
 
 struct ProcessorTerminate : public std::exception {
-    ProcessorTerminate(ProcessorTerminateReason reason = ProcessorTerminateReason::SUCCESS) : reason_(reason) {}
+    explicit ProcessorTerminate(ProcessorTerminateReason reason = ProcessorTerminateReason::SUCCESS) : reason_(reason) {}
     ProcessorTerminateReason reason_;
 };
 }


```

---

## [26/50] ID: CPP_0206 | C/C++ (T)
- **Rule ID:** `cppcheck/variableScope`
- **Result:** `PASS`
- **Target File:** `services/implementation/src/device_manager_service_impl.cpp`
- **Warning:** The scope of the variable 'hmlEnable160M' can be reduced.

### Buggy Snippet
```cpp
int DeviceManagerServiceImpl::OpenAuthSession(const std::string& deviceId,
    const std::map<std::string, std::string> &bindParam)
{
    if (bindParam.find(PARAM_KEY_IS_SERVICE_BIND) != bindParam.end() &&
        bindParam.at(PARAM_KEY_IS_SERVICE_BIND) == DM_VAL_TRUE) {
        CHECK_NULL_RETURN(listener_, ERR_DM_FAILED);
        if (IsNumberString(deviceId)) {
            return listener_->OpenAuthSessionWithPara(std::stoll(deviceId));
        } else {
            LOGE("OpenAuthSession failed");
            return ERR_DM_FAILED;
        }
    }
    bool hmlEnable160M = false;
    int32_t hmlActionId = 0;
    int invalidSessionId = -1;
    JsonObject jsonObject = GetExtraJsonObject(bindParam);
    if (jsonObject.IsDiscarded()) {
        LOGE("extra string not a json type.");
        return invalidSessionId;
    }
    if (softbusConnector_ == nullptr) {
        return invalidSessionId;
    }
    if (IsHmlSessionType(jsonObject)) {
        auto ret = GetHmlInfo(jsonObject, hmlEnable160M, hmlActionId);
        if (ret != DM_OK) {
            LOGE("OpenAuthSession failed, GetHmlInfo failed.");
            return ret;
        }
        LOGI("hmlActionId %{public}d, hmlEnable160M %{public}d", hmlActionId, hmlEnable160M);
        CHECK_NULL_RETURN(listener_, ERR_DM_FAILED);
        return listener_->OpenAuthSessionWithPara(deviceId, hmlActionId, hmlEnable160M);
    } else {
        return softbusConnector_->GetSoftbusSession()->OpenAuthSession(deviceId);
    }
}
```

### Patch
```diff
// File: services/implementation/src/device_manager_service_impl.cpp
--- a/services/implementation/src/device_manager_service_impl.cpp
+++ b/services/implementation/src/device_manager_service_impl.cpp
@@ -1642,8 +1642,6 @@
             return ERR_DM_FAILED;
         }
     }
-    bool hmlEnable160M = false;
-    int32_t hmlActionId = 0;
     int invalidSessionId = -1;
     JsonObject jsonObject = GetExtraJsonObject(bindParam);
     if (jsonObject.IsDiscarded()) {
@@ -1654,6 +1652,8 @@
         return invalidSessionId;
     }
     if (IsHmlSessionType(jsonObject)) {
+        bool hmlEnable160M = false;
+        int32_t hmlActionId = 0;
         auto ret = GetHmlInfo(jsonObject, hmlEnable160M, hmlActionId);
         if (ret != DM_OK) {
             LOGE("GetHmlInfo failed.");


```

---

## [27/50] ID: CPP_0284 | C/C++ (T)
- **Rule ID:** `cppcheck/uninitvar`
- **Result:** `PASS`
- **Target File:** `components/nstackx/nstackx_congestion/platform/unix/qdisc/nstackx_qdisc.c`
- **Warning:** Uninitialized variable: ret

### Buggy Snippet
```cpp
static int32_t GetQdiscUsedLength(const char *devName, int32_t protocol, int32_t *len)
{
    int32_t sockFd;
    int32_t ret;
    int32_t sendNetlinkRequestCount = SEND_NETLINK_REQUEST_COUNT;
    struct NlmsgCallback nlcb;
    QdiscArg qdiscArg;
    QdiscValue qdiscValue = {0};
    qdiscArg.ifIndex = (int32_t)if_nametoindex(devName);
    qdiscArg.protocol = protocol;

    nlcb.nlcb = ProcessQdiscInfo;
    nlcb.arg = &qdiscArg;
    nlcb.value = &qdiscValue;

    sockFd = NetlinkSocketInit();
    if (sockFd < 0) {
        return NSTACKX_EFAILED;
    }

    while (sendNetlinkRequestCount > 0) {
        ret = SendNetlinkRequest(sockFd, qdiscArg.ifIndex, RTM_GETQDISC);
        if (ret == NSTACKX_EOK) {
            ret = RecvNetlinkResponse(sockFd, &nlcb);
            if (ret == NSTACKX_EOK) {
                break;
            }
        }
        sendNetlinkRequestCount--;
    }
    if (ret == NSTACKX_EOK) {
        *len = qdiscValue.qlen;
    }
    if (close(sockFd) < 0)  {
        LOGE(TAG, "close failed.");
        return NSTACKX_EFAILED;
    }

    return ret;
}
```

### Patch
```diff
// File: components/nstackx/nstackx_congestion/platform/unix/qdisc/nstackx_qdisc.c
--- a/components/nstackx/nstackx_congestion/platform/unix/qdisc/nstackx_qdisc.c
+++ b/components/nstackx/nstackx_congestion/platform/unix/qdisc/nstackx_qdisc.c
@@ -99,7 +99,7 @@
 static int32_t GetQdiscUsedLength(const char *devName, int32_t protocol, int32_t *len)
 {
     int32_t sockFd;
-    int32_t ret;
+    int32_t ret = NSTACKX_EFAILED;
     int32_t sendNetlinkRequestCount = SEND_NETLINK_REQUEST_COUNT;
     struct NlmsgCallback nlcb;
     QdiscArg qdiscArg;


```

---

## [28/50] ID: CPP_0047 | C/C++ (T)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `PASS`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/mediacodec/capbilities/audio_decoder.cpp`
- **Warning:** Local variable 'ret' shadows outer variable

### Buggy Snippet
```cpp
int32_t AudioDecoder::Config(const SampleInfo &sampleInfo, CodecUserData *codecUserData)
{
    CHECK_AND_RETURN_RET_LOG(decoder_ != nullptr, AVCODEC_SAMPLE_ERR_ERROR, "Decoder is null");
    CHECK_AND_RETURN_RET_LOG(codecUserData != nullptr, AVCODEC_SAMPLE_ERR_ERROR, "Invalid param: codecUserData");

    // Configure audio decoder
    int32_t ret = Configure(sampleInfo);
    CHECK_AND_RETURN_RET_LOG(ret == AVCODEC_SAMPLE_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Configure failed");

    // SetCallback for audio decoder
    ret = SetCallback(codecUserData);
    CHECK_AND_RETURN_RET_LOG(
        ret == AVCODEC_SAMPLE_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Set callback failed, ret: %{public}d", ret);

    // Prepare audio decoder
    {
        int ret = OH_AudioCodec_Prepare(decoder_);
        CHECK_AND_RETURN_RET_LOG(ret == AV_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Prepare failed, ret: %{public}d", ret);
    }

    return AVCODEC_SAMPLE_ERR_OK;
}
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/mediacodec/capbilities/audio_decoder.cpp
--- a/ohos_YYEVA/library/src/main/cpp/mediacodec/capbilities/audio_decoder.cpp
+++ b/ohos_YYEVA/library/src/main/cpp/mediacodec/capbilities/audio_decoder.cpp
@@ -98,8 +98,8 @@
 
     // Prepare audio decoder
     {
-        int ret = OH_AudioCodec_Prepare(decoder_);
-        CHECK_AND_RETURN_RET_LOG(ret == AV_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Prepare failed, ret: %{public}d", ret);
+        int prepareRet = OH_AudioCodec_Prepare(decoder_);
+        CHECK_AND_RETURN_RET_LOG(prepareRet == AV_ERR_OK, AVCODEC_SAMPLE_ERR_ERROR, "Prepare failed, ret: %{public}d", prepareRet);
     }
 
     return AVCODEC_SAMPLE_ERR_OK;


```

---

## [29/50] ID: CPP_0297 | C/C++ (T)
- **Rule ID:** `cppcheck/uninitvar`
- **Result:** `PASS`
- **Target File:** `core/transmission/trans_channel/manager/src/trans_lane_manager.c`
- **Warning:** Uninitialized variable: socketItem->enableMultipath

### Buggy Snippet
```cpp
void TransGetMultipathReallocList(ListNode *multipathReallocList)
{
    if (multipathReallocList == NULL) {
        TRANS_LOGE(TRANS_SVC, "multipathReallocList is null");
        return;
    }
    if (g_socketChannelList == NULL) {
        TRANS_LOGE(TRANS_INIT, "socket info manager hasn't init.");
        return;
    }
    if (SoftBusMutexLock(&(g_socketChannelList->lock)) != SOFTBUS_OK) {
        TRANS_LOGE(TRANS_SVC, "lock failed");
        return;
    }
    SocketWithChannelInfo *socketItem;
    LIST_FOR_EACH_ENTRY(socketItem, &(g_socketChannelList->list), SocketWithChannelInfo, node) {
        TRANS_LOGI(TRANS_SVC, "sessionId=%{public}d, laneHandle=%{public}d, laneHandleReserve=%{public}d",
            socketItem->sessionId, socketItem->laneHandle, socketItem->laneHandleReserve);
        if (socketItem->enableMultipath &&
            IsSingleValidLaneHandle(socketItem->laneHandle, socketItem->laneHandleReserve)) {
            ReallocInfo *reallocNode = CreateReallocNode(socketItem);
            if (reallocNode == NULL) {
                continue;
            }
            TRANS_LOGI(TRANS_SVC, "multipath need realloc second lane, sessionId=%{public}d", socketItem->sessionId);
            ListAdd(multipathReallocList, &(reallocNode->node));
        }
    }
    (void)SoftBusMutexUnlock(&(g_socketChannelList->lock));
}
```

### Patch
```diff
// File: core/transmission/trans_channel/manager/src/trans_lane_manager.c
--- a/core/transmission/trans_channel/manager/src/trans_lane_manager.c
+++ b/core/transmission/trans_channel/manager/src/trans_lane_manager.c
@@ -1163,7 +1163,7 @@
         TRANS_LOGE(TRANS_SVC, "lock failed");
         return;
     }
-    SocketWithChannelInfo *socketItem;
+    SocketWithChannelInfo *socketItem = NULL;
     LIST_FOR_EACH_ENTRY(socketItem, &(g_socketChannelList->list), SocketWithChannelInfo, node) {
         TRANS_LOGI(TRANS_SVC, "sessionId=%{public}d, laneHandle=%{public}d, laneHandleReserve=%{public}d",
             socketItem->sessionId, socketItem->laneHandle, socketItem->laneHandleReserve);


```

---

## [30/50] ID: CPP_0228 | C/C++ (T)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `PASS`
- **Target File:** `adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c`
- **Warning:** Possible null pointer dereference: it

### Buggy Snippet
```cpp
static void GetGattcCallback(int32_t clientId, SoftBusGattcCallback *cb)
{
    CONN_CHECK_AND_RETURN_LOGE(g_softBusGattcManager != NULL, CONN_BLE, "GattcManager is null");
    CONN_CHECK_AND_RETURN_LOGE(SoftBusMutexLock(&g_softBusGattcManager->lock) == SOFTBUS_OK,
        CONN_BLE, "lock fail, clientId=%{public}d", clientId);
    SoftBusGattcManager *it = NULL;
    LIST_FOR_EACH_ENTRY(it, &g_softBusGattcManager->list, SoftBusGattcManager, node) {
        if (it->clientId == clientId) {
            *cb = it->callback;
            break;
        }
    }

    (void)SoftBusMutexUnlock(&g_softBusGattcManager->lock);
}
```

### Patch
```diff
// File: adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
--- a/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
+++ b/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
@@ -221,12 +221,13 @@
 
 static void GetGattcCallback(int32_t clientId, SoftBusGattcCallback *cb)
 {
+    CONN_CHECK_AND_RETURN_LOGE(cb != NULL, CONN_BLE, "cb is null");
     CONN_CHECK_AND_RETURN_LOGE(g_softBusGattcManager != NULL, CONN_BLE, "GattcManager is null");
     CONN_CHECK_AND_RETURN_LOGE(SoftBusMutexLock(&g_softBusGattcManager->lock) == SOFTBUS_OK,
         CONN_BLE, "lock fail, clientId=%{public}d", clientId);
     SoftBusGattcManager *it = NULL;
     LIST_FOR_EACH_ENTRY(it, &g_softBusGattcManager->list, SoftBusGattcManager, node) {
-        if (it->clientId == clientId) {
+        if (it != NULL && it->clientId == clientId) {
             *cb = it->callback;
             break;
         }


```

---

## [31/50] ID: CPP_0185 | C/C++ (T)
- **Rule ID:** `cppcheck/useStlAlgorithm`
- **Result:** `PASS`
- **Target File:** `interfaces/cj/kits/src/device_manager_utils.cpp`
- **Warning:** Consider using std::find_if algorithm instead of a raw loop.

### Buggy Snippet
```cpp
const std::string &GetDeviceTypeById(DmDeviceType type)
{
    const static std::pair<const DmDeviceType, const std::string &> mapArray[] = {
        {DEVICE_TYPE_UNKNOWN, std::string(DEVICE_TYPE_UNKNOWN_STRING)},
        {DEVICE_TYPE_PHONE, std::string(DEVICE_TYPE_PHONE_STRING)},
        {DEVICE_TYPE_PAD, std::string(DEVICE_TYPE_PAD_STRING)},
        {DEVICE_TYPE_TV, std::string(DEVICE_TYPE_TV_STRING)},
        {DEVICE_TYPE_CAR, std::string(DEVICE_TYPE_CAR_STRING)},
        {DEVICE_TYPE_WATCH, std::string(DEVICE_TYPE_WATCH_STRING)},
        {DEVICE_TYPE_WIFI_CAMERA, std::string(DEVICE_TYPE_WIFICAMERA_STRING)},
        {DEVICE_TYPE_PC, std::string(DEVICE_TYPE_PC_STRING)},
        {DEVICE_TYPE_SMART_DISPLAY, std::string(DEVICE_TYPE_SMART_DISPLAY_STRING)},
        {DEVICE_TYPE_2IN1, std::string(DEVICE_TYPE_2IN1_STRING)},
        {DEVICE_TYPE_GLASSES, std::string(DEVICE_TYPE_GLASSES_STRING)},
    };
    for (const auto& item : mapArray) {
        if (item.first == type) {
            return item.second;
        }
    }
    return mapArray[0].second;
}
```

### Patch
```diff
// File: interfaces/cj/kits/src/device_manager_utils.cpp
--- a/interfaces/cj/kits/src/device_manager_utils.cpp
+++ b/interfaces/cj/kits/src/device_manager_utils.cpp
@@ -14,6 +14,7 @@
  */
 #include "device_manager_utils.h"
 
+#include <algorithm>
 #include <string>
 #include <map>
 #include <mutex>
@@ -200,10 +201,10 @@
         {DEVICE_TYPE_2IN1, std::string(DEVICE_TYPE_2IN1_STRING)},
         {DEVICE_TYPE_GLASSES, std::string(DEVICE_TYPE_GLASSES_STRING)},
     };
-    for (const auto& item : mapArray) {
-        if (item.first == type) {
-            return item.second;
-        }
+    auto it = std::find_if(std::begin(mapArray), std::end(mapArray),
+                           [type](const auto& item) { return item.first == type; });
+    if (it != std::end(mapArray)) {
+        return it->second;
     }
     return mapArray[0].second;
 }


```

---

## [32/50] ID: CPP_0229 | C/C++ (T)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `PASS`
- **Target File:** `adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c`
- **Warning:** Possible null pointer dereference: it

### Buggy Snippet
```cpp
int32_t SoftbusGattcUnRegister(int32_t clientId)
{
    CONN_LOGI(CONN_BLE, "clientId=%{public}d", clientId);
    int32_t ret = SOFTBUS_OK;
    if (BleGattcUnRegister(clientId) != SOFTBUS_OK) {
        CONN_LOGE(CONN_BLE, "BleGattcUnRegister err");
        ret = SOFTBUS_GATTC_INTERFACE_FAILED;
    }
    CONN_CHECK_AND_RETURN_RET_LOGE(g_softBusGattcManager != NULL, SOFTBUS_INVALID_PARAM,
        CONN_BLE, "GattcManager is null");
    CONN_CHECK_AND_RETURN_RET_LOGE(SoftBusMutexLock(&g_softBusGattcManager->lock) == SOFTBUS_OK,
        SOFTBUS_LOCK_ERR, CONN_BLE, "lock fail, clientId=%{public}d", clientId);
    SoftBusGattcManager *it = NULL;
    SoftBusGattcManager *next = NULL;
    LIST_FOR_EACH_ENTRY_SAFE(it, next, &g_softBusGattcManager->list, SoftBusGattcManager, node) {
        if (it->clientId == clientId) {
            ListDelete(&it->node);
            SoftBusFree(it);
            break;
        }
    }
    (void)SoftBusMutexUnlock(&g_softBusGattcManager->lock);
    SoftbusGattcDeleteMacAddrFromList(clientId);
    return ret;
}
```

### Patch
```diff
// File: adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
--- a/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
+++ b/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_client.c
@@ -265,7 +265,7 @@
     SoftBusGattcManager *it = NULL;
     SoftBusGattcManager *next = NULL;
     LIST_FOR_EACH_ENTRY_SAFE(it, next, &g_softBusGattcManager->list, SoftBusGattcManager, node) {
-        if (it->clientId == clientId) {
+        if (it != NULL && it->clientId == clientId) {
             ListDelete(&it->node);
             SoftBusFree(it);
             break;


```

---

## [33/50] ID: CPP_0331 | C/C++ (T)
- **Rule ID:** `cppcheck/stlIfStrFind`
- **Result:** `PASS`
- **Target File:** `services/media_backup_extension/src/restore/photo_album_dao.cpp`
- **Warning:** Inefficient usage of string::find() in condition; string::starts_with() could be faster.

### Buggy Snippet
```cpp
/**
 * @brief Build PhotoAlbumRowData from lPath.
 */
PhotoAlbumDao::PhotoAlbumRowData PhotoAlbumDao::BuildAlbumInfoByLPath(const std::string &lPath)
{
    int32_t albumType = static_cast<int32_t>(PhotoAlbumType::SOURCE);
    int32_t albumSubType = static_cast<int32_t>(PhotoAlbumSubType::SOURCE_GENERIC);

    std::string target = "/Pictures/Users/";
    std::transform(target.begin(), target.end(), target.begin(), ::tolower);
    std::string lPathLower = lPath;
    std::transform(lPathLower.begin(), lPathLower.end(), lPathLower.begin(), ::tolower);
    if (lPathLower.find(target) == 0) {
        albumType = static_cast<int32_t>(PhotoAlbumType::USER);
        albumSubType = static_cast<int32_t>(PhotoAlbumSubType::USER_GENERIC);
    }
    return this->BuildAlbumInfoByLPath(lPath, albumType, albumSubType);
}
```

### Patch
```diff
// File: services/media_backup_extension/src/restore/photo_album_dao.cpp
--- a/services/media_backup_extension/src/restore/photo_album_dao.cpp
+++ b/services/media_backup_extension/src/restore/photo_album_dao.cpp
@@ -435,7 +435,7 @@
     std::transform(target.begin(), target.end(), target.begin(), ::tolower);
     std::string lPathLower = lPath;
     std::transform(lPathLower.begin(), lPathLower.end(), lPathLower.begin(), ::tolower);
-    if (lPathLower.find(target) == 0) {
+    if (lPathLower.starts_with(target)) {
         albumType = static_cast<int32_t>(PhotoAlbumType::USER);
         albumSubType = static_cast<int32_t>(PhotoAlbumSubType::USER_GENERIC);
     }


```

---

## [34/50] ID: CPP_0323 | C/C++ (T)
- **Rule ID:** `cppcheck/identicalInnerCondition`
- **Result:** `PASS`
- **Target File:** `frameworks/services/media_async_worker/src/medialibrary_period_worker.cpp`
- **Warning:** Identical inner 'if' condition is always true.

### Buggy Snippet
```cpp
if (periodWorkerInstance_ == nullptr) {
        lock_guard<mutex> lockGuard(instanceMtx_);
        if (periodWorkerInstance_ == nullptr) {
            periodWorkerInstance_ = shared_ptr<MediaLibraryPeriodWorker>(new MediaLibraryPeriodWorker());
            periodWorkerInstance_->Init();
        }
    }
    return periodWorkerInstance_;
}
```

### Patch
```diff
// File: frameworks/services/media_async_worker/src/medialibrary_period_worker.cpp
--- a/frameworks/services/media_async_worker/src/medialibrary_period_worker.cpp
+++ b/frameworks/services/media_async_worker/src/medialibrary_period_worker.cpp
@@ -35,12 +35,10 @@
 
 shared_ptr<MediaLibraryPeriodWorker> MediaLibraryPeriodWorker::GetInstance()
 {
+    lock_guard<mutex> lockGuard(instanceMtx_);
     if (periodWorkerInstance_ == nullptr) {
-        lock_guard<mutex> lockGuard(instanceMtx_);
-        if (periodWorkerInstance_ == nullptr) {
-            periodWorkerInstance_ = shared_ptr<MediaLibraryPeriodWorker>(new MediaLibraryPeriodWorker());
-            periodWorkerInstance_->Init();
-        }
+        periodWorkerInstance_ = shared_ptr<MediaLibraryPeriodWorker>(new MediaLibraryPeriodWorker());
+        periodWorkerInstance_->Init();
     }
     return periodWorkerInstance_;
 }


```

---

## [35/50] ID: CPP_0346 | C/C++ (T)
- **Rule ID:** `cppcheck/functionStatic`
- **Result:** `PASS`
- **Target File:** `NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp`
- **Warning:** Technically the member function 'MSDRadixSort::InsertionSort' can be static (but you may consider moving to unnamed namespace).

### Buggy Snippet
```cpp
// MSD基数排序（递归实现）
class MSDRadixSort {
private:
    // 递归排序函数
    void MsdSort(vector<int> &arr, int left, int right, int digit, int maxDigit)
    {
        const int digitCount = 10; // 0-9
        const int numBuckets = 11;
        if (left >= right || digit > maxDigit) {
            return;
        }

        int n = right - left + 1;
        if (n <= SMALL_ARRAY_THRESHOLD) {
            // 小数组使用插入排序
            InsertionSort(arr, left, right);
            return;
        }

        // 计数数组
        vector<int> count(digitCount + 1, 0); // 0-9 + 一个额外位置

        // 临时数组
        vector<int> temp(n);

        // 统计频率（处理digit=0的情况）
        for (int i = left; i <= right; i++) {
            int d = (digit == 0) ? 0 : GetDigit(arr[i], digit);
            count[d + 1]++; // +1为负数预留位置
        }

        // 计算起始位置
        for (int i = 1; i < numBuckets; i++) {
            count[i] += count[i - 1];
        }

        // 排序到临时数组
        for (int i = left; i <= right; i++) {
            int d = (digit == 0) ? 0 : GetDigit(arr[i], digit);
            temp[count[d]++] = arr[i];
        }

        // 复制回原数组
        for (int i = left; i <= right; i++) {
            arr[i] = temp[i - left];
        }

        // 递归排序每个桶
        int start = left;
        for (int i = 0; i < DECIMAL_BASE; i++) {
            int end = left + count[i] - 1;
            if (start <= end) {
                MsdSort(arr, start, end, digit - 1, maxDigit);
                start = end + 1;
            }
        }
    }

    void InsertionSort(vector<int> &arr, int left, int right)
    {
        for (int i = left + 1; i <= right; i++) {
            int key = arr[i];
            int j = i - 1;

            while (j >= left && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    int GetDigit(int num, int d)
    {
        for (int i = 1; i < d; i++) {
            num /= DECIMAL_BASE;
        }
        return num % DECIMAL_BASE;
    }

    int GetMaxDigits(const vector<int> &arr)
    {
        if (arr.empty()) {
            return 0;
        }

        int maxVal = *max_element(arr.begin(), arr.end());
        int digits = 0;

        while (maxVal > 0) {
            digits++;
            maxVal /= DECIMAL_BASE;
        }

        return max(1, digits);
    }

public:
    void Sort(vector<int> &arr)
    {
        if (arr.size() <= 1) {
            return;
        }

        int maxDigits = GetMaxDigits(arr);
        MsdSort(arr, 0, arr.size() - 1, maxDigits, maxDigits);
    }
};
```

### Patch
```diff
// File: NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
--- a/NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
+++ b/NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
@@ -1607,7 +1607,7 @@
         }
     }
 
-    void InsertionSort(vector<int> &arr, int left, int right)
+    static void InsertionSort(vector<int> &arr, int left, int right)
     {
         for (int i = left + 1; i <= right; i++) {
             int key = arr[i];


```

---

## [36/50] ID: CPP_0288 | C/C++ (T)
- **Rule ID:** `cppcheck/memleak`
- **Result:** `PASS`
- **Target File:** `components/nstackx/nstackx_util/platform/unix/sys_epoll.c`
- **Warning:** Memory leak: taskList

### Buggy Snippet
```cpp
static int32_t AddTaskToList(EpollTask *task)
{
    if (task == NULL) {
        return NSTACKX_EINVAL;
    }

    if (!g_isInit) {
        if (pthread_mutex_lock(&g_taskListMutex) != 0) {
            LOGE(TAG, "lock g_taskListMutex failed");
            return NSTACKX_EFAILED;
        }
        if (!g_isInit) {
            ListInitHead(&g_epollTaskList);
            g_isInit = true;
        }
        (void)pthread_mutex_unlock(&g_taskListMutex);
    }

    TaskList *taskListCheck = GetTaskFromList(task);
    if (taskListCheck != NULL) {
        LOGE(TAG, "taskListCheck GetTaskFromList failed");
        return NSTACKX_EFAILED;
    }
    TaskList *taskList = calloc(1, sizeof(TaskList));
    if (taskList == NULL) {
        LOGE(TAG, "calloc failed");
        return NSTACKX_EFAILED;
    }
    taskList->task = task;
    if (pthread_mutex_lock(&g_taskListMutex) != 0) {
        free(taskList);
        LOGE(TAG, "lock g_taskListMutex failed");
        return NSTACKX_EFAILED;
    }
    ListInsertTail(&g_epollTaskList, &taskList->list);
    (void)pthread_mutex_unlock(&g_taskListMutex);

    return NSTACKX_EOK;
}
```

### Patch
```diff
// File: components/nstackx/nstackx_util/platform/unix/sys_epoll.c
--- a/components/nstackx/nstackx_util/platform/unix/sys_epoll.c
+++ b/components/nstackx/nstackx_util/platform/unix/sys_epoll.c
@@ -111,8 +111,8 @@
     }
     taskList->task = task;
     if (pthread_mutex_lock(&g_taskListMutex) != 0) {
+        LOGE(TAG, "lock g_taskListMutex failed");
         free(taskList);
-        LOGE(TAG, "lock g_taskListMutex failed");
         return NSTACKX_EFAILED;
     }
     ListInsertTail(&g_epollTaskList, &taskList->list);


```

---

## [37/50] ID: CPP_0340 | C/C++ (T)
- **Rule ID:** `cppcheck/identicalInnerCondition`
- **Result:** `PASS`
- **Target File:** `services/media_mtp/src/mtp_storage_manager.cpp`
- **Warning:** Identical inner 'if' condition is always true.

### Buggy Snippet
```cpp
std::shared_ptr<MtpStorageManager> MtpStorageManager::instance_ = nullptr;
std::mutex MtpStorageManager::mutex_;

std::shared_ptr<MtpStorageManager> MtpStorageManager::GetInstance()
{
    if (instance_ == nullptr) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (instance_ == nullptr) {
            instance_ = std::make_shared<MtpStorageManager>();
        }
    }
    return instance_;
}
```

### Patch
```diff
// File: services/media_mtp/src/mtp_storage_manager.cpp
--- a/services/media_mtp/src/mtp_storage_manager.cpp
+++ b/services/media_mtp/src/mtp_storage_manager.cpp
@@ -48,11 +48,9 @@
 
 std::shared_ptr<MtpStorageManager> MtpStorageManager::GetInstance()
 {
+    std::lock_guard<std::mutex> lock(mutex_);
     if (instance_ == nullptr) {
-        std::lock_guard<std::mutex> lock(mutex_);
-        if (instance_ == nullptr) {
-            instance_ = std::make_shared<MtpStorageManager>();
-        }
+        instance_ = std::make_shared<MtpStorageManager>();
     }
     return instance_;
 }


```

---

## [38/50] ID: CPP_0165 | C/C++ (T)
- **Rule ID:** `cppcheck/variableScope`
- **Result:** `PASS`
- **Target File:** `vap/vap_module/src/main/cpp/mix/src.cpp`
- **Warning:** The scope of the variable 'colorStr' can be reduced.

### Buggy Snippet
```cpp
/*
 * Copyright (C) 2024 Huawei Device Co., Ltd.
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

#include "src.h"
#include "log.h"
#include "common_const.h"

using namespace CommonConst;

std::map<std::string, SrcType> Src::string2SrcType = {
    {"unknown", SrcType::UNKNOWN}, {"img", SrcType::IMG}, {"txt", SrcType::TXT}};

std::map<std::string, LoadType> Src::string2LoadType = {
    {"unknown", LoadType::UNKNOWN}, {"net", LoadType::NET}, {"local", LoadType::LOCAL}};

std::map<std::string, FitType> Src::string2FitType = {{"fitXY", FitType::FIT_XY}, {"centerFull", FitType::CENTER_FULL}};

std::map<std::string, Style> Src::string2Style = {{"default", Style::DEFAULT}, {"b", Style::BOLD}};

Src::Src(json jsonSrc)
{
    srcId = jsonSrc.at("srcId").get<std::string>();
    std::string tmpStr = jsonSrc.at("srcType").get<std::string>();
    srcType = stringToSrcTypeFunc(tmpStr);
    tmpStr = jsonSrc.at("loadType").get<std::string>();
    loadType = stringToLoadTypeFunc(tmpStr);
    srcTag = jsonSrc.at("srcTag").get<std::string>();
    txt = srcTag;
    std::string colorStr;
    if (jsonSrc.find("color") != jsonSrc.end()) {
        colorStr = jsonSrc.at("color").get<std::string>();
        colorStr.erase(0, 1); // 去掉字符串开头的 #
        color = std::stoi(colorStr, nullptr, TWO_TIME_EIGHT);
        if (((color >> THREE_TIME_EIGHT) & 0xff) == 0) {
            color |= 0xff << THREE_TIME_EIGHT;
        }
    }
    if (jsonSrc.find("style") != jsonSrc.end()) {
        tmpStr = jsonSrc.at("style").get<std::string>();
        style = stringToStyleFunc(tmpStr);
    }
    w = jsonSrc.at("w").get<int32_t>();
    h = jsonSrc.at("h").get<int32_t>();
    tmpStr = jsonSrc.at("fitType").get<std::string>();
    fitType = stringToFitTypeFunc(tmpStr);
}
```

### Patch
```diff
// File: vap/vap_module/src/main/cpp/mix/src.cpp
--- a/vap/vap_module/src/main/cpp/mix/src.cpp
+++ b/vap/vap_module/src/main/cpp/mix/src.cpp
@@ -38,9 +38,8 @@
     loadType = stringToLoadTypeFunc(tmpStr);
     srcTag = jsonSrc.at("srcTag").get<std::string>();
     txt = srcTag;
-    std::string colorStr;
     if (jsonSrc.find("color") != jsonSrc.end()) {
-        colorStr = jsonSrc.at("color").get<std::string>();
+        std::string colorStr = jsonSrc.at("color").get<std::string>();
         colorStr.erase(0, 1); // 去掉字符串开头的 #
         color = std::stoi(colorStr, nullptr, TWO_TIME_EIGHT);
         if (((color >> THREE_TIME_EIGHT) & 0xff) == 0) {


```

---

## [39/50] ID: CPP_0293 | C/C++ (T)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `PASS`
- **Target File:** `core/connection/br/src/softbus_conn_br_connection.c`
- **Warning:** Local variable 'ret' shadows outer variable

### Buggy Snippet
```cpp
static int32_t BrOnReferenceRequest(uint32_t connectionId, ReferenceCount *referenceCount)
{
    int32_t delta = referenceCount->delta;
    int32_t peerRc = referenceCount->peerRc;
    ConnBrConnection *connection = ConnBrGetConnectionById(connectionId);
    CONN_CHECK_AND_RETURN_RET_LOGE(connection != NULL,
        SOFTBUS_INVALID_PARAM, CONN_BR, "conn not exist, id=%{public}u", connectionId);

    int32_t ret = SoftBusMutexLock(&connection->lock);
    if (ret != SOFTBUS_OK) {
        CONN_LOGE(CONN_BR, "lock fail, connId=%{public}u, error=%{public}d", connectionId, ret);
        ConnBrReturnConnection(&connection);
        return SOFTBUS_LOCK_ERR;
    }
    bool isOccupied =  connection->isOccupied;
    (void)SoftBusMutexUnlock(&connection->lock);
    ConnBrReturnConnection(&connection);

    if (delta < 0 && isOccupied) {
        CONN_LOGI(CONN_BR, "is occupied, request process later, connId=%{public}u", connectionId);
        ReferenceCount *referenceParam = (ReferenceCount *)SoftBusMalloc(sizeof(ReferenceCount));
        if (referenceParam == NULL) {
            CONN_LOGE(CONN_BR, "malloc buffer fail, connId=%{public}u", connectionId);
            return SOFTBUS_MALLOC_ERR;
        }
        referenceParam->delta = delta;
        referenceParam->peerRc = peerRc;

        int32_t ret = ConnPostMsgToLooper(&g_brConnectionAsyncHandler, MSG_CONNECTION_UPDATE_PEER_RC,
            connectionId, 0, referenceParam, WAIT_TIMEOUT_TRY_AGAIN);
        if (ret != SOFTBUS_OK) {
            CONN_LOGE(CONN_BR, "post msg fail, connId=%{public}u, error=%{public}d", connectionId, ret);
            SoftBusFree(referenceParam);
            return ret;
        }
        return SOFTBUS_OK;
    }
    return NotifyReferenceRequest(connectionId, delta, peerRc);
}
```

### Patch
```diff
// File: core/connection/br/src/softbus_conn_br_connection.c
--- a/core/connection/br/src/softbus_conn_br_connection.c
+++ b/core/connection/br/src/softbus_conn_br_connection.c
@@ -634,12 +634,12 @@
         referenceParam->delta = delta;
         referenceParam->peerRc = peerRc;
 
-        int32_t ret = ConnPostMsgToLooper(&g_brConnectionAsyncHandler, MSG_CONNECTION_UPDATE_PEER_RC,
+        int32_t postRet = ConnPostMsgToLooper(&g_brConnectionAsyncHandler, MSG_CONNECTION_UPDATE_PEER_RC,
             connectionId, 0, referenceParam, WAIT_TIMEOUT_TRY_AGAIN);
-        if (ret != SOFTBUS_OK) {
-            CONN_LOGE(CONN_BR, "post msg fail, connId=%{public}u, error=%{public}d", connectionId, ret);
+        if (postRet != SOFTBUS_OK) {
+            CONN_LOGE(CONN_BR, "post msg fail, connId=%{public}u, error=%{public}d", connectionId, postRet);
             SoftBusFree(referenceParam);
-            return ret;
+            return postRet;
         }
         return SOFTBUS_OK;
     }


```

---

## [40/50] ID: CPP_0305 | C/C++ (T)
- **Rule ID:** `cppcheck/stlIfStrFind`
- **Result:** `PASS`
- **Target File:** `frameworks/innerkitsimpl/media_library_helper/src/media_file_utils.cpp`
- **Warning:** Inefficient usage of string::find() in condition; string::starts_with() could be faster.

### Buggy Snippet
```cpp
bool MediaFileUtils::IsPhotoTablePath(const string &path)
{
    if (path.empty() || path.size() <= ROOT_MEDIA_DIR.size()) {
        return false;
    }

    if (path.find(ROOT_MEDIA_DIR) == string::npos) {
        return false;
    }

    string relativePath = path.substr(ROOT_MEDIA_DIR.size());

    const vector<string> photoPathVector = {
        PHOTO_BUCKET, PIC_DIR_VALUES, VIDEO_DIR_VALUES, CAMERA_DIR_VALUES
    };
    for (auto &photoPath : photoPathVector) {
        if (relativePath.find(photoPath) == 0) {
            return true;
        }
    }
    return false;
}
```

### Patch
```diff
// File: frameworks/innerkitsimpl/media_library_helper/src/media_file_utils.cpp
--- a/frameworks/innerkitsimpl/media_library_helper/src/media_file_utils.cpp
+++ b/frameworks/innerkitsimpl/media_library_helper/src/media_file_utils.cpp
@@ -1917,7 +1917,7 @@
     }
 
     string relativePath = path.substr(ROOT_MEDIA_DIR.size());
-    if ((relativePath.find(DOCS_PATH) == 0)) {
+    if (relativePath.starts_with(DOCS_PATH)) {
         return true;
     }
     return false;
@@ -1939,7 +1939,7 @@
         PHOTO_BUCKET, PIC_DIR_VALUES, VIDEO_DIR_VALUES, CAMERA_DIR_VALUES
     };
     for (auto &photoPath : photoPathVector) {
-        if (relativePath.find(photoPath) == 0) {
+        if (relativePath.starts_with(photoPath)) {
             return true;
         }
     }


```

---

## [41/50] ID: CPP_0052 | C/C++ (T)
- **Rule ID:** `cppcheck/noExplicitConstructor`
- **Result:** `PASS`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/ohos/napi_async_handler.h`
- **Warning:** Class 'NapiScope' has a constructor with 1 argument that is not explicit.

### Buggy Snippet
```cpp
/*
 * Copyright (C) 2025 Huawei Device Co., Ltd.
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

#ifndef UTILS_NAPI_ASYNC_HANDLER_H
#define UTILS_NAPI_ASYNC_HANDLER_H
#include "native_common.h"
#include "ohos_log.h"
#include <functional>
#include <memory>
#include <napi/native_api.h>
#include <cinttypes>
#include <string>
#include "napi_wrapper.h"

class NapiWrapper;

class NapiScope {
public:
    NapiScope(napi_env env) : env_(env)
    {
        napi_status status = napi_open_handle_scope(env_, &scope_);
        if (status != napi_ok) {
            LOGE("Failed to open handle scope");
            return;
        }
    }
    ~NapiScope()
    {
        napi_close_handle_scope(env_, scope_);
    }

private:
    napi_env env_;
    napi_handle_scope scope_;
};
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/ohos/napi_async_handler.h
--- a/ohos_YYEVA/library/src/main/cpp/ohos/napi_async_handler.h
+++ b/ohos_YYEVA/library/src/main/cpp/ohos/napi_async_handler.h
@@ -28,7 +28,7 @@
 
 class NapiScope {
 public:
-    NapiScope(napi_env env) : env_(env)
+    explicit NapiScope(napi_env env) : env_(env)
     {
         napi_status status = napi_open_handle_scope(env_, &scope_);
         if (status != napi_ok) {


```

---

## [42/50] ID: CPP_0359 | C/C++ (T)
- **Rule ID:** `cppcheck/missingReturn`
- **Result:** `PASS`
- **Target File:** `appnative/src/main/cpp/rouletteZoom/zoom_calculate.cpp`
- **Warning:** Found an exit path from function with non-void return type that has missing return statement

### Buggy Snippet
```cpp
/**
 * 获取当前模式的等效焦距数组index与变焦点数组index的差
 */
int ZoomCalculate::getFocalIndexDiff(const ZoomStruct* state, double zoomValue, int count)
{
    int diff = ARRAY_ZERO;
    if (state->isSupportedCycleClickZoom && count != ARRAY_ZERO) {
        if (state->cycleClickZoomLength == 1 && zoomValue >= state->cycleClickZoomValArr[0]) {
            return diff + 1;
        }
        for (int i = 0;i < state->cycleClickZoomLength; i++) {
            if (zoomValue >= state->cycleClickZoomValArr[i]) {
              diff++;
            }
        }
        return diff;
    }
    if (!state->isSupportedEquivalentFocalBigText || count == ARRAY_ZERO) {
        return diff;
    }
    if (count == ARRAY_ONE) {
        if (zoomValue < POINT_ZOOM_ONE) {
            return diff;
        } else {
            return diff + ARRAY_ONE;
        }
    }
    if (count == ARRAY_THREE) {
        if (zoomValue < POINT_ZOOM_ONE) {
            return diff;
        } else if (zoomValue >= POINT_ZOOM_ONE && zoomValue < POINT_ZOOM_TWO) {
            return diff + ARRAY_ONE;
        } else if (zoomValue >= POINT_ZOOM_TWO && zoomValue < POINT_ZOOM_THREE) {
            return diff + ARRAY_TWO;
        } else if (zoomValue >= POINT_ZOOM_THREE) {
            return diff + ARRAY_THREE;
        }
    }
}
```

### Patch
```diff
// File: appnative/src/main/cpp/rouletteZoom/zoom_calculate.cpp
--- a/appnative/src/main/cpp/rouletteZoom/zoom_calculate.cpp
+++ b/appnative/src/main/cpp/rouletteZoom/zoom_calculate.cpp
@@ -314,6 +314,7 @@
             return diff + ARRAY_THREE;
         }
     }
+    return diff;
 }
 
 /**


```

---

## [43/50] ID: CPP_0121 | C/C++ (T)
- **Rule ID:** `cppcheck/functionStatic`
- **Result:** `PASS`
- **Target File:** `socketio_2.x/library/src/main/cpp/client_socket.cpp`
- **Warning:** Technically the member function 'ClientSocket::OnOpen' can be static (but you may consider moving to unnamed namespace).

### Buggy Snippet
```cpp
class ClientSocket {
public:
    ClientSocket() noexcept {}

    void OnOpen(SocketIOClient* client)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> OnOpen classId: %{public}s", 
                     client ? client->classIdStr.c_str() : "null");
            
        if (client && client->tsfnOnOpenCall) {
            napi_acquire_threadsafe_function(client->tsfnOnOpenCall);
            napi_call_threadsafe_function(client->tsfnOnOpenCall, nullptr, napi_tsfn_blocking);
        }
    }

    void OnFail(SocketIOClient* client)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> OnFail classId: %{public}s", 
                     client ? client->classIdStr.c_str() : "null");
            
        if (client && client->tsfnFailCall) {
            napi_acquire_threadsafe_function(client->tsfnFailCall);
            napi_call_threadsafe_function(client->tsfnFailCall, nullptr, napi_tsfn_blocking);
        }
    }

    void OnReconnecting(SocketIOClient* client)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> OnReconnecting classId: %{public}s", 
                     client ? client->classIdStr.c_str() : "null");
            
        if (client && client->tsfnReconnectingCall) {
            napi_acquire_threadsafe_function(client->tsfnReconnectingCall);
            napi_call_threadsafe_function(client->tsfnReconnectingCall, nullptr, napi_tsfn_blocking);
        }
    }

    // 待回传unsigned两个参数
    void OnReconnect(unsigned attempts, unsigned delay, SocketIOClient* client)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> OnReconnect classId: %{public}s", 
                     client ? client->classIdStr.c_str() : "null");
            
        if (client && client->tsfnReconnectCall) {
            napi_acquire_threadsafe_function(client->tsfnReconnectCall);
            napi_call_threadsafe_function(client->tsfnReconnectCall, nullptr, napi_tsfn_blocking);
        }
    }

    void on_close(sio::client::close_reason const &reason, SocketIOClient* client)
    {
        std::string reasonString = "";
        if (reason == sio::client::close_reason_normal) {
            reasonString = "close_reason_normal";
        } else if (reason == sio::client::close_reason_drop) {
            reasonString = "close_reason_drop";
        }
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> on_close classId: %{public}s", 
                     client ? client->classIdStr.c_str() : "null");
        
        if (client && client->tsfnCloseCall) {
            std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
            if (!localThreadSafeInfo) {
                OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_close]localThreadSafeInfo is null");
                return;
            }
            localThreadSafeInfo->result = reasonString;
            
            napi_acquire_threadsafe_function(client->tsfnCloseCall);
            napi_call_threadsafe_function(client->tsfnCloseCall, localThreadSafeInfo.release(), napi_tsfn_blocking);
        }
    }

    void on_socket_open(std::string const &nsp, SocketIOClient* client)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------>0 on_socket_open %{public}s classId: %{public}s",
                     nsp.c_str(), client ? client->classIdStr.c_str() : "null");
        
        if (client && client->tsfnOnSocketioOpenCall) {
            std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
            if (!localThreadSafeInfo) {
                OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_socket_open]localThreadSafeInfo is null");
                return;
            }
            localThreadSafeInfo->result = nsp;
            
            napi_acquire_threadsafe_function(client->tsfnOnSocketioOpenCall);
            napi_call_threadsafe_function(client->tsfnOnSocketioOpenCall, localThreadSafeInfo.release(), napi_tsfn_blocking);
        }
    }

    void on_socket_close(std::string const &nsp, SocketIOClient* client)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> on_socket_close classId: %{public}s", 
                     client ? client->classIdStr.c_str() : "null");
        
        if (client && client->tsfnOnCloseCall) {
            std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
            if (!localThreadSafeInfo) {
                OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_socket_close]localThreadSafeInfo is null");
                return;
            }
            localThreadSafeInfo->result = nsp;

            napi_acquire_threadsafe_function(client->tsfnOnCloseCall);
            napi_call_threadsafe_function(client->tsfnOnCloseCall, localThreadSafeInfo.release(), napi_tsfn_blocking);
        }
    }

    void on_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                               sio::message::list const &message, bool needAck, sio::message::list &ack_message,
                               SocketIOClient* client)
    {
        client->isOnce = false;
        handler_event_listener_aux(context, name, message, needAck,
            ack_message, client);
    }
    
    void on_binary_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                               sio::message::list const &message, bool needAck, sio::message::list &ack_message,
                               SocketIOClient* client)
    {
        client->isOnce = false;
        handler_binary_event_listener_aux(context, name, message, needAck,
            ack_message, client);
    }

    void once_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                                 sio::message::list const &message, bool needAck, sio::message::list &ack_message,
                                 SocketIOClient* client)
    {
        client->isOnce = true;
        handler_event_listener_aux(context, name, message, needAck,
            ack_message, client);
    }

    void on_multi_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                                    sio::message::list const &message, bool needAck, sio::message::list &ack_message,
                                    SocketIOClient* client)
    {
        client->isOnce = false;
        handler_multi_event_listener_aux(context, name, message, needAck, ack_message, client);
    }

    void on_error_listener(sio::message::ptr const &message, SocketIOClient* client)
    {
        std::string error_string = "on error";
        
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> on_error_listener classId: %{public}s", 
                     client ? client->classIdStr.c_str() : "null");
        
        if (client && client->tsfnOnErrorCall) {
            std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
            if (!localThreadSafeInfo) {
                OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_error_listener]localThreadSafeInfo is null");
                return;
            }
            localThreadSafeInfo->result = error_string;
            
            napi_acquire_threadsafe_function(client->tsfnOnErrorCall);
            napi_call_threadsafe_function(client->tsfnOnErrorCall, localThreadSafeInfo.release(), napi_tsfn_blocking);
        }
    }

    std::string build_emit_message_json_old(sio::message::list const &list)
    {
        std::string str;
        str += "{";
        if (list.at(0)->get_flag() == sio::message::flag_object) {
            std::map<std::string, sio::message::ptr> messageMap = list.at(0)->get_map();
            for (auto it : messageMap) {
                if (messageMap.begin()->first != it.first) {
                    str += ",";
                }
                str += "\"" + it.first + "\":" + get_message_value(it.second);
            }
        } else {
            str += "\"message\":" + get_message_value(list.at(0));
        }
        str += "}";
        return str;
    }

    std::string build_emit_message_json(sio::message::list const &list)
    {
        std::string str;
        if (list.size() == 1) {
            str = build_emit_message_json_old(list);
        } else {
            str += "[";
            for (int16_t index = 0; index < list.size(); index++) {
                std::string tmp;
                if ((list.at(index)->get_flag() == sio::message::flag_binary)) {
                    tmp = std::string("\"") + *(list.at(index)->get_binary()) + "\"";
                } else {
                    tmp = get_message_value(list.at(index));
                }
                str += tmp;
                if (index < list.size() - 1) {
                    str += ",";
                }
            }
            str += "]";
        }
        return str;
    }

    void on_emit_callback(SocketIOClient* client, std::string const &ackName, sio::message::list const &list)
    {
        OH_LOG_Print(LOG_APP,   LOG_INFO,   LOG_DOMAIN,   LOG_TAG, "SOCKETIO_TAG------> 0 on_emit_callback -------");

        if (!client) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "client not found for emit callback");
            return;
        }
        
        napi_ref on_emit_listener_call_ref = client->on_emit_listener_call_ref_map[ackName.c_str()];
        if (on_emit_listener_call_ref == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "on_emit_listener_call_ref is null");
            return;
        }
        std::string messageJson = build_emit_message_json(list);
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> 1 on_emit_callback %{public}s",
                     messageJson.c_str());

        std::unique_ptr<ThreadSafeInfo> localThreadSafeInfo = std::make_unique<ThreadSafeInfo>();
        if (!localThreadSafeInfo) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_emit_callback]localThreadSafeInfo is null");
            return;
        }
        localThreadSafeInfo->result = messageJson;

        // 使用与该事件名绑定的 TSFN（队列 FIFO 出队），确保同名并发 emit 分别回调
        auto qIt = client->on_emit_tsfn_map.find(ackName);
        if (qIt == client->on_emit_tsfn_map.end() || qIt->second.empty()) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[on_emit_callback] tsfn queue empty for event");
            return;
        }
        napi_threadsafe_function tsfn = qIt->second.front();
        qIt->second.pop_front();
        if (qIt->second.empty()) {
            client->on_emit_tsfn_map.erase(qIt);
        }

        napi_acquire_threadsafe_function(tsfn);
        napi_call_threadsafe_function(tsfn, localThreadSafeInfo.release(), napi_tsfn_blocking);
        napi_release_threadsafe_function(tsfn, napi_tsfn_release);
    }
};
```

### Patch
```diff
// File: socketio_2.x/library/src/main/cpp/client_socket.cpp
--- a/socketio_2.x/library/src/main/cpp/client_socket.cpp
+++ b/socketio_2.x/library/src/main/cpp/client_socket.cpp
@@ -371,7 +371,7 @@
 public:
     ClientSocket() noexcept {}
 
-    void OnOpen(SocketIOClient* client)
+    static void OnOpen(SocketIOClient* client)
     {
         OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> OnOpen classId: %{public}s", 
                      client ? client->classIdStr.c_str() : "null");


```

---

## [44/50] ID: CPP_0345 | C/C++ (T)
- **Rule ID:** `cppcheck/functionStatic`
- **Result:** `PASS`
- **Target File:** `NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp`
- **Warning:** Technically the member function 'OptimizedRadixSort::GetDigit' can be static (but you may consider moving to unnamed namespace).

### Buggy Snippet
```cpp
// 优化的LSD基数排序，支持2的幂作为基数
class OptimizedRadixSort {
private:
    // 获取数字在指定基数下的第k位
    int GetDigit(int num, int k, int radix)
    {
        int shiftAmount = k * static_cast<int>(log2(radix));
        return (num >> shiftAmount) & (radix - 1);
    }

    // 计算最大位数
    int GetMaxDigits(int maxVal, int radix)
    {
        int digits = 0;
        while (maxVal > 0 && radix != 0) {
            digits++;
            maxVal /= radix;
        }
        return max(1, digits);
    }

public:
    // 通用基数排序，radix必须是2的幂（2,4,8,16,32,64,128,256）
    void Sort(vector<int> &arr, int radix = DEFAULT_RADIX)
    {
        int n = arr.size();
        if (n <= 1) {
            return;
        }

        // 找到最大值
        int maxVal = *max_element(arr.begin(), arr.end());

        // 计算最大位数
        int maxDigits = GetMaxDigits(maxVal, radix);

        // 临时数组
        vector<int> output(n);

        // 对每一位进行计数排序
        for (int digit = 0; digit < maxDigits; digit++) {
            vector<int> count(radix, 0);

            // 统计频率
            for (int i = 0; i < n; i++) {
                int d = GetDigit(arr[i], digit, radix);
                count[d]++;
            }

            // 计算位置
            for (int i = 1; i < radix; i++) {
                count[i] += count[i - 1];
            }

            // 从后向前填充
            for (int i = n - 1; i >= 0; i--) {
                int d = GetDigit(arr[i], digit, radix);
                output[--count[d]] = arr[i];
            }

            // 交换数组
            arr.swap(output);
        }
    }
};
```

### Patch
```diff
// File: NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
--- a/NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
+++ b/NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp
@@ -1466,7 +1466,7 @@
 class OptimizedRadixSort {
 private:
     // 获取数字在指定基数下的第k位
-    int GetDigit(int num, int k, int radix)
+    static int GetDigit(int num, int k, int radix)
     {
         int shiftAmount = k * static_cast<int>(log2(radix));
         return (num >> shiftAmount) & (radix - 1);


```

---

## [45/50] ID: CPP_0044 | C/C++ (T)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `PASS`
- **Target File:** `ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.cpp`
- **Warning:** Function parameter 'effects' should be passed by const reference.

### Buggy Snippet
```cpp
EvaSrcMap::EvaSrcMap(list<shared_ptr<Effect>> effects) {
    for (shared_ptr<Effect> effect: effects) {
        auto src = make_shared<EvaSrc>(effect);
        if (src->srcType != EvaSrc::UNKNOWN) {
            map[src->srcId] = src;
        } else {
            src = nullptr;
        }
    }
//    list<Effect>::iterator it;
//    for (it = effects.begin(); it != effects.end(); ++it) {
//        EvaSrc *src = new EvaSrc(it);
//        if (src->srcType != EvaSrc::UNKNOWN) {
//            map[src->srcId] = *src;
//        } else {
//            src = nullptr;
//        }
//    }
}
```

### Patch
```diff
// File: ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.cpp
--- a/ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.cpp
+++ b/ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.cpp
@@ -8,7 +8,7 @@
 
 }
 
-EvaSrcMap::EvaSrcMap(list<shared_ptr<Effect>> effects) {
+EvaSrcMap::EvaSrcMap(const list<shared_ptr<Effect>>& effects) {
     for (shared_ptr<Effect> effect: effects) {
         auto src = make_shared<EvaSrc>(effect);
         if (src->srcType != EvaSrc::UNKNOWN) {

--- a/ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.h
+++ b/ohos_YYEVA/library/src/main/cpp/bean/evasrcmap.h
@@ -13,7 +13,7 @@
 public:
     map<string, shared_ptr<EvaSrc>> map;
     EvaSrcMap();
-    EvaSrcMap(list<shared_ptr<Effect>> effects);
+    EvaSrcMap(const list<shared_ptr<Effect>>& effects);
 
     ~EvaSrcMap();
 };


```

---

## [46/50] ID: CPP_0314 | C/C++ (T)
- **Rule ID:** `cppcheck/identicalInnerCondition`
- **Result:** `PASS`
- **Target File:** `frameworks/innerkitsimpl/medialibrary_data_extension/src/medialibrary_related_system_state_manager.cpp`
- **Warning:** Identical inner 'if' condition is always true.

### Buggy Snippet
```cpp
if (medialibraryRelatedSystemStateManager == nullptr) { // 双重检查锁定 (DCLP)
        std::lock_guard<std::mutex> lock(mutex_);
        if (medialibraryRelatedSystemStateManager == nullptr) {
            medialibraryRelatedSystemStateManager = std::make_shared<MedialibraryRelatedSystemStateManager>();
            int32_t ret = medialibraryRelatedSystemStateManager->Init();
            CHECK_AND_RETURN_RET_LOG(ret == ERR_OK, nullptr, "failed to init medialibraryRelatedSystemStateManager");
        }
    }
    return medialibraryRelatedSystemStateManager;
}
```

### Patch
```diff
// File: frameworks/innerkitsimpl/medialibrary_data_extension/src/medialibrary_related_system_state_manager.cpp
--- a/frameworks/innerkitsimpl/medialibrary_data_extension/src/medialibrary_related_system_state_manager.cpp
+++ b/frameworks/innerkitsimpl/medialibrary_data_extension/src/medialibrary_related_system_state_manager.cpp
@@ -35,15 +35,18 @@
  
 std::shared_ptr<MedialibraryRelatedSystemStateManager> MedialibraryRelatedSystemStateManager::GetInstance()
 {
-    if (medialibraryRelatedSystemStateManager == nullptr) { // 双重检查锁定 (DCLP)
+    auto instance = medialibraryRelatedSystemStateManager;
+    if (instance == nullptr) { // 双重检查锁定 (DCLP)
         std::lock_guard<std::mutex> lock(mutex_);
-        if (medialibraryRelatedSystemStateManager == nullptr) {
+        instance = medialibraryRelatedSystemStateManager;
+        if (instance == nullptr) {
             medialibraryRelatedSystemStateManager = std::make_shared<MedialibraryRelatedSystemStateManager>();
             int32_t ret = medialibraryRelatedSystemStateManager->Init();
             CHECK_AND_RETURN_RET_LOG(ret == ERR_OK, nullptr, "failed to init medialibraryRelatedSystemStateManager");
+            instance = medialibraryRelatedSystemStateManager;
         }
     }
-    return medialibraryRelatedSystemStateManager;
+    return instance;
 }
 
 int32_t MedialibraryRelatedSystemStateManager::Init()


```

---

## [47/50] ID: CPP_0224 | C/C++ (T)
- **Rule ID:** `cppcheck/shadowVariable`
- **Result:** `PASS`
- **Target File:** `services/service/src/relationshipsyncmgr/relationship_sync_mgr.cpp`
- **Warning:** Local variable 'payloadItem' shadows outer variable

### Buggy Snippet
```cpp
bool RelationShipChangeMsg::FromSyncFrontOrBackUserIdPayLoad(const cJSON *payloadJson)
{
    if (payloadJson == NULL) {
        LOGE("payloadJson is null.");
        return false;
    }

    int32_t arraySize = cJSON_GetArraySize(payloadJson);
    if (arraySize < SYNC_FRONT_OR_BACK_USERID_PAYLOAD_MIN_LEN ||
        arraySize > SYNC_FRONT_OR_BACK_USERID_PAYLOAD_MAX_LEN) {
        LOGE("Payload invalid, the size is %{public}d.", arraySize);
        return false;
    }

    cJSON *payloadItem = cJSON_GetArrayItem(payloadJson, 0);
    CHECK_NULL_RETURN(payloadItem, false);
    uint32_t userIdNum = 0;
    if (cJSON_IsNumber(payloadItem)) {
        uint8_t val = static_cast<uint8_t>(payloadItem->valueint);
        this->syncUserIdFlag = (((val >> NEED_RSP_MASK_OFFSET) & 0x1) == 0x1);
        this->isNewEvent = (((val >> IS_NEW_USER_SYNC_MASK_OFFSET) & 0x1) == 0x1);
        userIdNum = ((static_cast<uint8_t>(payloadItem->valueint)) & FOREGROUND_USERID_LEN_MASK);
    }

    int32_t effectiveLen = static_cast<int32_t>((userIdNum + 1) * USERID_BYTES);
    if (effectiveLen > arraySize) {
        LOGE("payload userIdNum invalid, userIdNum: %{public}u, arraySize: %{public}d", userIdNum, arraySize);
        return false;
    }

    uint16_t tempUserId = 0;
    bool isForegroundUser = false;
    for (int32_t idx = 1; idx < effectiveLen; idx++) {
        cJSON *payloadItem = cJSON_GetArrayItem(payloadJson, idx);
        CHECK_NULL_RETURN(payloadItem, false);
        if (!cJSON_IsNumber(payloadItem)) {
            LOGE("Payload invalid, user id not integer");
            return false;
        }
        if ((idx - 1) % USERID_BYTES == 0) {
            tempUserId |= (static_cast<uint8_t>(payloadItem->valueint));
        }
        if ((idx - 1) % USERID_BYTES == 1) {
            tempUserId |= (static_cast<uint8_t>(payloadItem->valueint) << BITS_PER_BYTE);
            tempUserId &= FRONT_OR_BACK_USER_FLAG_MASK;
            isForegroundUser = (((static_cast<uint8_t>(payloadItem->valueint) & FRONT_OR_BACK_FLAG_MASK) >>
                FRONT_OR_BACK_USER_FLAG_OFFSET) == 0b1);
            UserIdInfo userIdInfo(isForegroundUser, tempUserId);
            this->userIdInfos.push_back(userIdInfo);
            tempUserId = 0;
            isForegroundUser = false;
        }
    }
    return GetBroadCastId(payloadJson, userIdNum);
}
```

### Patch
```diff
// File: services/service/src/relationshipsyncmgr/relationship_sync_mgr.cpp
--- a/services/service/src/relationshipsyncmgr/relationship_sync_mgr.cpp
+++ b/services/service/src/relationshipsyncmgr/relationship_sync_mgr.cpp
@@ -837,7 +837,7 @@
     uint16_t tempUserId = 0;
     bool isForegroundUser = false;
     for (int32_t idx = 1; idx < effectiveLen; idx++) {
-        cJSON *payloadItem = cJSON_GetArrayItem(payloadJson, idx);
+        payloadItem = cJSON_GetArrayItem(payloadJson, idx);
         CHECK_NULL_RETURN(payloadItem, false);
         if (!cJSON_IsNumber(payloadItem)) {
             LOGE("Payload invalid, user id not integer");


```

---

## [48/50] ID: CPP_0234 | C/C++ (T)
- **Rule ID:** `cppcheck/nullPointer`
- **Result:** `PASS`
- **Target File:** `adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c`
- **Warning:** Possible null pointer dereference: it

### Buggy Snippet
```cpp
static void FindCallbackAndNotifyConnected(int32_t connId, int32_t attrHandle, SoftBusGattsCallback *callback)
{
    CONN_CHECK_AND_RETURN_LOGE(SoftBusMutexLock(&g_softBusGattsManager.lock) == SOFTBUS_OK,
        CONN_BLE, "lock fail, handle=%{public}d", attrHandle);
    ServerService *it = NULL;
    ServerService *target = NULL;
    LIST_FOR_EACH_ENTRY(it, &g_softBusGattsManager.services, ServerService, node) {
        if (it->callback.isConcernedAttrHandle != NULL && it->callback.isConcernedAttrHandle(it->handle, attrHandle)) {
            target = it;
            break;
        }
    }
    if (target == NULL)  {
        CONN_LOGW(CONN_BLE, "unconcerned handle=%{public}d", attrHandle);
        (void)SoftBusMutexUnlock(&g_softBusGattsManager.lock);
        return;
    }

    ServerConnection *connection = GetServerConnectionByConnIdUnsafe(connId);
    if (connection == NULL) {
        CONN_LOGE(CONN_BLE, "conn not exist, connId=%{public}d", connId);
        (void)SoftBusMutexUnlock(&g_softBusGattsManager.lock);
        return;
    }

    connection->handle = target->handle; // Map connection to server
    if (!connection->notifyConnected && connection->mtu != 0) {
        if (target->callback.connectServerCallback != NULL) {
            target->callback.connectServerCallback(connId, &connection->btAddr);
        }
        if (target->callback.mtuChangeCallback != NULL) {
            target->callback.mtuChangeCallback(connId, connection->mtu);
        }
        connection->notifyConnected = true;
    }
    *callback = target->callback;
    (void)SoftBusMutexUnlock(&g_softBusGattsManager.lock);
}
```

### Patch
```diff
// File: adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c
--- a/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c
+++ b/adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c
@@ -532,7 +532,7 @@
     ServerService *it = NULL;
     ServerService *target = NULL;
     LIST_FOR_EACH_ENTRY(it, &g_softBusGattsManager.services, ServerService, node) {
-        if (it->callback.isConcernedAttrHandle != NULL && it->callback.isConcernedAttrHandle(it->handle, attrHandle)) {
+        if (it != NULL && it->callback.isConcernedAttrHandle != NULL && it->callback.isConcernedAttrHandle(it->handle, attrHandle)) {
             target = it;
             break;
         }


```

---

## [49/50] ID: CPP_0115 | C/C++ (T)
- **Rule ID:** `cppcheck/redundantAssignment`
- **Result:** `PASS`
- **Target File:** `ohos_vlc/library/src/main/cpp/media_player_wrapper.cpp`
- **Warning:** Variable 'status' is reassigned a value before the old one has been used.

### Buggy Snippet
```cpp
napi_value MediaPlayerWrapper::SetVideoOut(napi_env env, napi_callback_info info)
{
    napi_value arkTSVLCPlayer = nullptr;
    size_t argc = 1;
    napi_value args[1] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, &arkTSVLCPlayer, nullptr);
    
    MediaPlayerWrapper *player = nullptr;
    napi_status status = napi_unwrap(env, arkTSVLCPlayer, reinterpret_cast<void **>(&player));
    if (status != napi_ok || player == nullptr || player->instance_ == nullptr) {
        LOGE("napi_unwrap MediaPlayerWrapper failed!");
        return nullptr;
    }

    size_t length;
    status = napi_get_value_string_utf8(env, args[0], nullptr, 0, &length);
    std::string id(length, '\0');
    status = napi_get_value_string_utf8(env, args[0], &id[0], length + 1, &length);
    LOGD("id = %s, component = %p Window = = %p", id.c_str(), xMgr.GetNativeXcomponent(id), xMgr.GetNativeWindow(id));
    libvlc_media_player_set_ohos_nativewindow_ptr(player->instance_, xMgr.GetNativeWindow(id));
    return nullptr;
}
```

### Patch
```diff
// File: ohos_vlc/library/src/main/cpp/media_player_wrapper.cpp
--- a/ohos_vlc/library/src/main/cpp/media_player_wrapper.cpp
+++ b/ohos_vlc/library/src/main/cpp/media_player_wrapper.cpp
@@ -185,7 +185,7 @@
     }
 
     size_t length;
-    status = napi_get_value_string_utf8(env, args[0], nullptr, 0, &length);
+    napi_get_value_string_utf8(env, args[0], nullptr, 0, &length);
     std::string id(length, '\0');
     status = napi_get_value_string_utf8(env, args[0], &id[0], length + 1, &length);
     LOGD("id = %s, component = %p Window = = %p", id.c_str(), xMgr.GetNativeXcomponent(id), xMgr.GetNativeWindow(id));


```

---

## [50/50] ID: CPP_0033 | C/C++ (T)
- **Rule ID:** `cppcheck/passedByValue`
- **Result:** `PASS`
- **Target File:** `napi/settings/napi_settings_observer.cpp`
- **Warning:** Function parameter 'tableName' should be passed by const reference.

### Buggy Snippet
```cpp
if (this->cbInfo == nullptr) {
            return;
        }
        delete this->cbInfo;
        this->cbInfo = nullptr;
    }

    bool IsExistObserver(SettingsObserver* settingsObserver) {
        for (auto it = g_observerMap.begin(); it != g_observerMap.end(); ++it) {
            if (&(*(it->second)) == settingsObserver) {
                return true;
            }
        }
        return false;
    }

    std::shared_ptr<DataShareHelper> createDataShareHelper(
        napi_env env, sptr<IRemoteObject> token, std::string tableName)
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
        if (currentUserId > USERID_HELPER_NUMBER) {
            SETTING_LOG_INFO("user0 userId is %{public}d", tmpId);
        }
        std::string strUri = "datashare:///com.ohos.settingsdata.DataAbility";
        std::string strProxyUri = GetProxyUriStr(tableName, tmpId);
        OHOS::Uri proxyUri(strProxyUri);
        dataShareHelper = OHOS::DataShare::DataShareHelper::Creator(token, strProxyUri, "");
        if (!dataShareHelper) {
            SETTING_LOG_ERROR("dataShareHelper from proxy is null");
            dataShareHelper = OHOS::DataShare::DataShareHelper::Creator(token, strUri, "");
        } else {
            dataShareHelper->SetDataShareHelperExtUri(strUri);
        }
        return dataShareHelper;
    }

    void SettingsObserver::DoEventWork(SettingsObserver *settingsObserver)
    {
        SETTING_LOG_INFO("n_s_o_c_a_l");
        std::lock_guard<std::recursive_mutex> lockGuard(g_observerMapMutex);
        if (!IsExistObserver(settingsObserver) || settingsObserver == nullptr || settingsObserver->cbInfo == nullptr ||
            settingsObserver->toBeDelete) {
            SETTING_LOG_ERROR("uv_work: cbInfo invalid.");
            return;
        }

        napi_handle_scope scope = nullptr;
        napi_open_handle_scope(settingsObserver->cbInfo->env, &scope);
        napi_value callback = nullptr;
        napi_value undefined;
        napi_get_undefined(settingsObserver->cbInfo->env, &undefined);
        napi_value error = nullptr;
        napi_create_object(settingsObserver->cbInfo->env, &error);
        int unSupportCode = 802;
        napi_value errCode = nullptr;
        napi_create_int32(settingsObserver->cbInfo->env, unSupportCode, &errCode);
        napi_set_named_property(settingsObserver->cbInfo->env, error, "code", errCode);
        napi_value result[PARAM2] = {0};
        result[0] = error;
        result[1] = wrap_bool_to_js(settingsObserver->cbInfo->env, false);
        napi_get_reference_value(settingsObserver->cbInfo->env, settingsObserver->cbInfo->callbackRef,
            &callback);
        napi_value callResult;
        napi_call_function(settingsObserver->cbInfo->env, undefined, callback, PARAM2, result,
            &callResult);
        napi_close_handle_scope(settingsObserver->cbInfo->env, scope);
        SETTING_LOG_INFO("%{public}s, uv_work success.", __func__);
    }

    void SettingsObserver::OnChange()
    {
        SETTING_LOG_INFO("n_s_o_cl");
        std::lock_guard<std::recursive_mutex> lockGuard(g_observerMapMutex);
        if (this->cbInfo == nullptr || this->toBeDelete) {
            SETTING_LOG_ERROR("%{public}s, cbInfo is null, deleted: %{public}d", __func__, this->toBeDelete);
            return;
        }
        uv_loop_s* loop = nullptr;
        napi_get_uv_event_loop(cbInfo->env, &loop);
        if (loop == nullptr) {
            SETTING_LOG_ERROR("%{public}s, fail to get uv loop.", __func__);
            return;
        }
        auto work = new (std::nothrow) uv_work_t;
        if (work == nullptr) {
            SETTING_LOG_ERROR("%{public}s, fail to get uv work.", __func__);
            return;
        }
        work->data = reinterpret_cast<void*>(this);
        SettingsObserver* settingsObserver = reinterpret_cast<SettingsObserver*>(work->data);
        int ret = napi_send_event(cbInfo->env, std::bind(DoEventWork, settingsObserver), napi_eprio_high);
        if (ret != 0) {
            SETTING_LOG_ERROR("%{public}s, uv_queue_work failed.", __func__);
        }
        if (work != nullptr) {
            delete work;
            work = nullptr;
        }
    }

    int GetObserverIdStr()
    {
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
            SETTING_LOG_INFO("%{public}s, user id 100.", __func__);
        }
        return tmpId;
    }

    void CleanObserverMap(std::string key)
    {
        std::lock_guard<std::recursive_mutex> lockGuard(g_observerMapMutex);
        g_observerMap[key]->toBeDelete = true;
        g_observerMap[key] = nullptr;
        g_observerMap.erase(key);
    }

    void CleanUp(void* data)
    {
        SETTING_LOG_INFO("CleanUp");
        if (data == nullptr) {
            SETTING_LOG_WARN("CleanUp, data nullptr");
            return;
        }
        AsyncCallbackInfo* callbackInfo = reinterpret_cast<AsyncCallbackInfo*>(data);
        std::lock_guard<std::recursive_mutex> lockGuard(g_observerMapMutex);
        if (g_observerMap.find(callbackInfo->key) != g_observerMap.end() &&
            g_observerMap[callbackInfo->key] != nullptr) {
            SETTING_LOG_WARN("CleanUp key is %{public}s", callbackInfo->key.c_str());
            CleanObserverMap(callbackInfo->key);
            napi_delete_reference(callbackInfo->env, callbackInfo->callbackRef);
            callbackInfo->env = nullptr;
            callbackInfo->callbackRef = nullptr;
            delete callbackInfo;
        }
    }

    napi_value npai_settings_register_observer(napi_env env, napi_callback_info info)
    {
        SETTING_LOG_INFO("n_s_r_o");
        // Check the number of the arguments
        size_t argc = ARGS_FOUR;
        napi_value args[ARGS_FOUR] = {nullptr};
        NAPI_CALL(env, napi_get_cb_info(env, info, &argc, args, nullptr, nullptr));
        if (argc != ARGS_FOUR) {
            SETTING_LOG_ERROR("%{public}s, wrong number of arguments.", __func__);
            return wrap_bool_to_js(env, false);
        }

        // Check the value type of the arguments
        napi_valuetype valueType;
        NAPI_CALL(env, napi_typeof(env, args[PARAM0], &valueType));
        NAPI_ASSERT(env, valueType == napi_object, "Wrong argument[0] type. Object expected.");
        NAPI_CALL(env, napi_typeof(env, args[PARAM1], &valueType));
        NAPI_ASSERT(env, valueType == napi_string, "Wrong argument[1] type. String expected.");
        NAPI_CALL(env, napi_typeof(env, args[PARAM2], &valueType));
        NAPI_ASSERT(env, valueType == napi_string, "Wrong argument[2] type. String expected.");

        bool stageMode = false;
        if (napi_ok != OHOS::AbilityRuntime::IsStageContext(env, args[PARAM0], stageMode)) {
            SETTING_LOG_ERROR("%{public}s, not stage mode.", __func__);
            return wrap_bool_to_js(env, false);
        }
        AsyncCallbackInfo *callbackInfo = new AsyncCallbackInfo();
        if (callbackInfo == nullptr) {
            SETTING_LOG_ERROR("%{public}s, failed to get callbackInfo.", __func__);
            return wrap_bool_to_js(env, false);
        }

        std::lock_guard<std::recursive_mutex> lockGuard(g_observerMapMutex);
        callbackInfo->env = env;
        callbackInfo->key = unwrap_string_from_js(env, args[PARAM1]);
        callbackInfo->tableName = unwrap_string_from_js(env, args[PARAM2]);
        napi_create_reference(env, args[PARAM3], 1, &(callbackInfo->callbackRef));

        if (g_observerMap.find(callbackInfo->key) != g_observerMap.end() &&
        g_observerMap[callbackInfo->key] != nullptr) {
            SETTING_LOG_INFO("%{public}s, already registered.", __func__);
            napi_delete_reference(env, callbackInfo->callbackRef);
            delete callbackInfo;
            return wrap_bool_to_js(env, false);
        }
        auto contextS = OHOS::AbilityRuntime::GetStageModeContext(env, args[PARAM0]);
        if (contextS == nullptr) {
            SETTING_LOG_ERROR("get context is error.");
            delete callbackInfo;
            return wrap_bool_to_js(env, false);
        }
        auto dataShareHelper = createDataShareHelper(env, contextS->GetToken(),
                                                     callbackInfo->tableName);
        if (dataShareHelper == nullptr) {
            napi_delete_reference(env, callbackInfo->callbackRef);
            delete callbackInfo;
            return wrap_bool_to_js(env, false);
        }

        std::string strUri = GetStageUriStr(callbackInfo->tableName, GetObserverIdStr(), callbackInfo->key);
        OHOS::Uri uri(strUri);
        sptr<SettingsObserver> settingsObserver = sptr<SettingsObserver>
        (new (std::nothrow)SettingsObserver(callbackInfo));
        g_observerMap[callbackInfo->key] = settingsObserver;
        napi_add_env_cleanup_hook(env, CleanUp, callbackInfo);
        dataShareHelper->RegisterObserver(uri, settingsObserver);
        dataShareHelper->Release();
		
        return wrap_bool_to_js(env, true);
    }

    napi_value npai_settings_unregister_observer(napi_env env, napi_callback_info info)
    {
        SETTING_LOG_INFO("n_s_u_o");
        // Check the number of the arguments
        size_t argc = ARGS_THREE;
        napi_value args[ARGS_THREE] = {nullptr};
        NAPI_CALL(env, napi_get_cb_info(env, info, &argc, args, nullptr, nullptr));
        if (argc != ARGS_THREE) {
            SETTING_LOG_ERROR("%{public}s, wrong number of arguments.", __func__);
            return wrap_bool_to_js(env, false);
        }
        // Check the value type of the arguments
        napi_valuetype valueType;
        NAPI_CALL(env, napi_typeof(env, args[PARAM0], &valueType));
        NAPI_ASSERT(env, valueType == napi_object, "Wrong argument[0] type. Object expected.");
        NAPI_CALL(env, napi_typeof(env, args[PARAM1], &valueType));
        NAPI_ASSERT(env, valueType == napi_string, "Wrong argument[1] type. String expected.");
        NAPI_CALL(env, napi_typeof(env, args[PARAM2], &valueType));
        NAPI_ASSERT(env, valueType == napi_string, "Wrong argument[2] type. String expected.");

        bool stageMode = false;
        if (napi_ok != OHOS::AbilityRuntime::IsStageContext(env, args[PARAM0], stageMode)) {
            SETTING_LOG_ERROR("%{public}s, not stage mode.", __func__);
            return wrap_bool_to_js(env, false);
        }

        std::string key = unwrap_string_from_js(env, args[PARAM1]);
        std::string tableName = unwrap_string_from_js(env, args[PARAM2]);
        
        std::lock_guard<std::recursive_mutex> lockGuard(g_observerMapMutex);
        if (g_observerMap.find(key) == g_observerMap.end()) {
            SETTING_LOG_ERROR("%{public}s, null.", __func__);
            return wrap_bool_to_js(env, false);
        }
        
        if (g_observerMap[key] == nullptr) {
            g_observerMap.erase(key);
            return wrap_bool_to_js(env, false);
        }
        auto contextS = OHOS::AbilityRuntime::GetStageModeContext(env, args[PARAM0]);
        if (contextS == nullptr) {
            SETTING_LOG_ERROR("get context is error.");
            return wrap_bool_to_js(env, false);
        }
        auto dataShareHelper = createDataShareHelper(env, contextS->GetToken(), tableName);
        if (dataShareHelper == nullptr) {
            SETTING_LOG_ERROR("%{public}s, data share is null.", __func__);
            return wrap_bool_to_js(env, false);
        }
        std::string strUri = GetStageUriStr(tableName, GetObserverIdStr(), key);
        napi_remove_env_cleanup_hook(env, CleanUp, g_observerMap[key]->cbInfo);
        napi_delete_reference(g_observerMap[key]->cbInfo->env, g_observerMap[key]->cbInfo->callbackRef);
        dataShareHelper->UnregisterObserver(OHOS::Uri(strUri), g_observerMap[key]);
        dataShareHelper->Release();
        CleanObserverMap(key);
		
        return wrap_bool_to_js(env, true);
    }
}
```

### Patch
```diff
// File: napi/settings/napi_settings_observer.cpp
--- a/napi/settings/napi_settings_observer.cpp
+++ b/napi/settings/napi_settings_observer.cpp
@@ -56,7 +56,7 @@
     }
 
     std::shared_ptr<DataShareHelper> createDataShareHelper(
-        napi_env env, sptr<IRemoteObject> token, std::string tableName)
+        napi_env env, sptr<IRemoteObject> token, const std::string& tableName)
     {
         std::shared_ptr<OHOS::DataShare::DataShareHelper> dataShareHelper = nullptr;
         int currentUserId = -1;
@@ -265,7 +265,7 @@
         napi_add_env_cleanup_hook(env, CleanUp, callbackInfo);
         dataShareHelper->RegisterObserver(uri, settingsObserver);
         dataShareHelper->Release();
-		
+                
         return wrap_bool_to_js(env, true);
     }
 
@@ -324,7 +324,7 @@
         dataShareHelper->UnregisterObserver(OHOS::Uri(strUri), g_observerMap[key]);
         dataShareHelper->Release();
         CleanObserverMap(key);
-		
+                
         return wrap_bool_to_js(env, true);
     }
 }


```

---

