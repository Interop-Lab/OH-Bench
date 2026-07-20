# Oracle Verdict Audit - False Negatives (ArkTS)

## [1/50] ID: OH_0075 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/component/contactdetail/DetailInfoTelList.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct TelList {
  @Link @Watch('mPresenterChange') private mPresenter: DetailPresenter;
  @Link selectSimBuilder: SelectDialogBuilder;
  @Link maximum: number;
  @Link moreOptionsFlag: boolean;
  @State otherFlag: boolean = false;
  @State isPressedIndex: number = -1;
  @Prop telephoneTotal: number;
  @Prop meettingTotal: number;
  // other total
  @Prop otherTotal: number;
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;
  customParams: CustomizedParams = {};

  mPresenterChange() {
    if (this.meettingTotal > 0 || this.otherTotal > 0
    ) {
      this.otherFlag = true
    }
  }

  // 处理展开更多与未展开更多情况下分割线的显示
  isDividerShow(totalCount: number, index: number): Visibility {
    let dividerShow: Visibility = Visibility.None;
    if (!this.moreOptionsFlag && totalCount > this.maximum) {
      if (index === this.maximum - 1) {
        dividerShow = Visibility.None
      } else {
        dividerShow = Visibility.Visible
      }
    } else {
      if (index === totalCount - 1) {
        dividerShow = Visibility.None
      } else {
        dividerShow = Visibility.Visible
      }
    }
    return dividerShow
  }


  build() {
    if (!ArrayUtil.isEmpty<ContackPhoneSubInfoModel>(this.mPresenter.contactForm.phones)) {
      List() {
        LazyForEach(this.mPresenter.phoneDataSources, (item: ContactStrInterface, index: number) => {
          if (JSON.parse(item.data).data && this.itemVisible(index)) {
            ListItem() {
              Column() {
                TelListItem({
                  message: item.data,
                  mPresenter: $mPresenter,
                  selectSimBuilder: $selectSimBuilder,
                  index: item.index,
                  telephoneTotal: this.telephoneTotal
                })
                Divider()
                  .color($r('app.color.skin_comp_divider'))
                  .strokeWidth('1px')
                  .width('100%')
                  .visibility(this.isDividerShow(this.mPresenter.phoneDataSources.totalCount(), index))
                  .padding({ left: $r('sys.float.padding_level4'), right: $r('sys.float.padding_level4') })
              }
            }
            .height('undefined')
          }
        }, (item: ContactStrInterface, index: number) => JSON.stringify(item) + JSON.stringify(index))
      }
      .scrollBar(BarState.Off)
      .edgeEffect(EdgeEffect.None)
      .enableScrollInteraction(false)
    }
  }

  itemVisible(index: number): boolean {
    return this.moreOptionsFlag ? (index < this.mPresenter.phoneDataSources.totalCount()) : (index < this.maximum);
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/component/contactdetail/DetailInfoTelList.ets
--- a/entry/src/main/ets/component/contactdetail/DetailInfoTelList.ets
+++ b/entry/src/main/ets/component/contactdetail/DetailInfoTelList.ets
@@ -89,6 +89,7 @@
 /**
  * Phone List
  */
+@Reusable
 @Component
 struct TelList {
   @Link @Watch('mPresenterChange') private mPresenter: DetailPresenter;


```

## [2/50] ID: OH_0015 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct RecordView {
  @Link private mPresenter: any
  @LocalStorageProp('breakpoint') curBp: string = 'sm';
  recordType: number = 0;

  build() {
    List({ space: 0, initialIndex: 0 }) {
      LazyForEach(this.recordType === 0 ? this.mPresenter.mAllCallRecordListDataSource :
      this.mPresenter.mMissCallRecordListDataSource, (item, index: number) => {
        ListItem() {
          ContactItem({ mPresenter: $mPresenter, item: item });
        }
        .height($r("app.float.id_item_height_max"))
      }, item => item.id)
    }
    .divider({
      strokeWidth: 1,
      color: $r('sys.color.ohos_id_color_list_separator'),
      startMargin: $r("app.float.id_item_height_sm"),
      endMargin: $r("app.float.id_card_margin_max"),
    })
    .width("100%")
    .margin({ bottom: this.curBp === 'lg' ? '110vp' : 0 })
    .flexShrink(1)
    .listDirection(Axis.Vertical)
    .edgeEffect(EdgeEffect.Spring)
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets
--- a/entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets
+++ b/entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets
@@ -103,6 +103,7 @@
   sendMessage, Copy, EditBeforeCall, BlockList, DeleteCallLogs
 }
 
+@Reusable
 @Component
 struct ContactItem {
   @State mIndexPresenter: IndexPresenter = IndexPresenter.getInstance();


```

## [3/50] ID: OH_0180 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-local-var-to-replace-state-var`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/pages/dialogPlus.ets`
- **Warning:** Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
aboutToAppear() {
    this.count = 0;
    this.initStatus = Constants.INIT_NEED_TO_WAIT;
    this.result = [];
    this.reqPerms = this.want.parameters['ohos.user.grant.permission'];
    this.accessTokenId = this.want.parameters['ohos.aafwk.param.callerToken'];
    if (this.reqPerms == undefined || this.accessTokenId == undefined || this.reqPerms.length == 0) {
      Log.info('invalid parameters');
      this.initStatus = Constants.INIT_NEED_TO_TERMINATED;
      return;
    }
    Log.info(`request permission: ${JSON.stringify(this.reqPerms)}.`);
    Log.info('permission state=' + JSON.stringify(this.want.parameters['ohos.user.grant.permission.state']));
    this.result = new Array(this.reqPerms.length).fill(-1);
    this.getPasteBoardInfo();
    let bundleName: string = this.want.parameters['ohos.aafwk.param.callerBundleName'];
    try {
      bundleManager.getBundleInfo(bundleName, bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_REQUESTED_PERMISSION)
        .then(bundleInfo => {
          this.reqPermissionDetails = bundleInfo.reqPermissionDetails;
          this.getGrantGroups(this.want.parameters['ohos.user.grant.permission.state']);
          this.getApplicationName(bundleName);
          this.dialogController?.open();
        }).catch((err: BusinessError) => {
          Log.error('getBundleInfo error :' + JSON.stringify(err));
          this.initStatus = Constants.INIT_NEED_TO_TERMINATED;
        })
    } catch (err) {
      Log.error('getBundleInfo error :' + JSON.stringify(err));
      this.initStatus = Constants.INIT_NEED_TO_TERMINATED;
    }
  }
```

### Patch
```diff
// File: permissionmanager/src/main/ets/pages/dialogPlus.ets
--- a/permissionmanager/src/main/ets/pages/dialogPlus.ets
+++ b/permissionmanager/src/main/ets/pages/dialogPlus.ets
@@ -67,7 +67,6 @@
   @State reqPerms: Array<Permission> = [];
   @State grantGroups: Array<GroupInfo> = [];
   @State userFixedFlag: number = 2; // means user fixed
-  @State grantStatus: number = -1;
   @State appName: string = '';
   @State locationFlag: number = Constants.LOCATION_NONE;
   @State reqPermissionDetails: bundleManager.ReqPermissionDetail[] = [];
@@ -290,24 +289,24 @@
   async privacyAccept(group: GroupInfo, accessTokenId: number, permissionList: string[], userFixedFlag: number) {
     let num = 0;
     group.permissions.forEach(async permission => {
-      this.grantStatus = -1;
+      let grantStatus = -1;
       if (showSubPermissionsGroup.indexOf(group.name) == -1) {
         if (group.name == 'LOCATION') {
           if (fuzzyMarks.includes(this.locationFlag) && permission === Permission.APPROXIMATELY_LOCATION) {
-            await this.operationPermission(true, accessTokenId, permission, userFixedFlag);
+            grantStatus = await this.operationPermission(true, accessTokenId, permission, userFixedFlag);
           }
           if (preciseMarks.includes(this.locationFlag) && permission === Permission.LOCATION) {
-            await this.operationPermission(true, accessTokenId, permission, userFixedFlag);
+            grantStatus = await this.operationPermission(true, accessTokenId, permission, userFixedFlag);
           }
         } else {
-          await this.operationPermission(true, accessTokenId, permission, userFixedFlag);
+          grantStatus = await this.operationPermission(true, accessTokenId, permission, userFixedFlag);
         }
       } else {
         if (permissionList.includes(permission)) {
-          await this.operationPermission(true, accessTokenId, permission, userFixedFlag);
-        }
-      }
-      if (this.grantStatus == abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED) {
+          grantStatus = await this.operationPermission(true, accessTokenId, permission, userFixedFlag);
+        }
+      }
+      if (grantStatus == abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED) {
         permissionList.forEach((req, idx) => {
           if (req == permission) {
             this.result[idx] = abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED;
@@ -334,22 +333,24 @@
     this.count ++;
   }
 
-  async operationPermission(status: boolean, token: number, permission: Permissions, flag: number) {
+  async operationPermission(status: boolean, token: number, permission: Permissions, flag: number): Promise<number> {
     if (status) {
       try {
         Log.info('grantUserGrantedPermission: ' + permission);
-        await abilityAccessCtrl.createAtManager().grantUserGrantedPermission(token, permission, flag).then(() => {
-          this.grantStatus = abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED;
-        })
+        await abilityAccessCtrl.createAtManager().grantUserGrantedPermission(token, permission, flag);
+        return abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED;
       } catch (err) {
         Log.error('failed to grant permission: ' + permission);
+        return -1;
       }
     } else {
       try {
         Log.info('revokeUserGrantedPermission: ' + permission)
         await abilityAccessCtrl.createAtManager().revokeUserGrantedPermission(token, permission, flag);
+        return -1;
       } catch (err) {
         Log.error('failed to revoke permission:' + permission);
+        return -1;
       }
     }
   }


```

## [4/50] ID: OH_0172 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-local-var-to-replace-state-var`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/pages/dialogPlus.ets`
- **Warning:** Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
if (this.reqPerms.includes(FUZZY_LOCATION_PERMISSION)) {
        this.locationFlag = Constants.LOCATION_FUZZY;
        if (this.reqPerms.includes(PRECISE_LOCATION_PERMISSION)) {
          this.locationFlag = Constants.LOCATION_BOTH_PRECISE;
          let fuzzyIndex = this.reqPerms.indexOf(FUZZY_LOCATION_PERMISSION);
          if (stateGroup[fuzzyIndex] == Constants.PASS_OPER) {
            this.locationFlag = Constants.LOCATION_UPGRADE;
          }
        }
      }
```

### Patch
```diff
// File: permissionmanager/src/main/ets/pages/dialogPlus.ets
--- a/permissionmanager/src/main/ets/pages/dialogPlus.ets
+++ b/permissionmanager/src/main/ets/pages/dialogPlus.ets
@@ -144,13 +144,14 @@
                         if (this.showReason()) {
                           Span($r('app.string.close_exact_position'))
                         } else {
-                          if (this.grantGroups[this.count >= this.grantGroups.length ? this.grantGroups.length - 1 : this.count].description.length > 0) {
-                            ForEach(this.grantGroups[this.count >= this.grantGroups.length ? this.grantGroups.length - 1 : this.count].description, (item: ResourceStr) => {
+                          let currentIndex = this.count >= this.grantGroups.length ? this.grantGroups.length - 1 : this.count;
+                          if (this.grantGroups[currentIndex].description.length > 0) {
+                            ForEach(this.grantGroups[currentIndex].description, (item: ResourceStr) => {
                               Span(item)
                             })
                             Span(this.punctuation())
                           }
-                          Span(this.grantGroups[this.count >= this.grantGroups.length ? this.grantGroups.length - 1 : (this.count + this.refresh - this.refresh)].reason)
+                          Span(this.grantGroups[currentIndex].reason)
                         }
                       }
                         .fontSize(Constants.DIALOG_DESP_FONT_SIZE)


```

## [5/50] ID: OH_0167 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let j = 0; j < routerData.length; j++) {
          if (res.reqPermissions.indexOf(routerData[j].permission) == -1) {
            continue
          }
          verifyAccessToken(res.appInfo.accessTokenId, routerData[j].permission).then((access) => {
            if (Number(access) === Constants.PERMISSION_INDEX) {
              if(boole){
                this.toggleIsOn[i] = true;
              }
            } else {
              if(boole){
                this.permissionNum--
              }
              boole = false;
              this.toggleIsOn[i] = false;
            }
          });
        }
```

### Patch
```diff
// File: permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
--- a/permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
+++ b/permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
@@ -167,8 +167,9 @@
                         _this.toggleIsOn[item.index] = true;
                       }
                       let num = Constants.PERMISSION_NUM;
-                      for(let key in _this.toggleIsOn){
-                        if(_this.toggleIsOn[key]){
+                      const toggleState = _this.toggleIsOn;
+                      for(let key in toggleState){
+                        if(toggleState[key]){
                           num++;
                         }
                       }
@@ -189,8 +190,9 @@
                         _this.toggleIsOn[item.index] = false;
                       }
                       let num = Constants.PERMISSION_NUM;
-                      for(let key in _this.toggleIsOn){
-                        if(_this.toggleIsOn[key]){
+                      const toggleState = _this.toggleIsOn;
+                      for(let key in toggleState){
+                        if(toggleState[key]){
                           num++;
                         }
                       }


```

## [6/50] ID: OH_0095 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/contacts/settings/ImportAndExport.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
{
{
{
                    HiLog.w(TAG, 'show simCount  ' + this.simCount + ' simNoCount  ' + this.simNoCount);
                  } else {
                    this.isShowSimEntry = false;
                    HiLog.w(TAG, 'not show simCount  ' + this.simCount + 'not simNoCount  ' + this.simNoCount);
                  }
                });
                HiLog.w(TAG, 'getSetupSimCardState Check sim');
              }
            } else {
              this.simFlag = true;
              simIccDiallingNumbers.getNumbersBySlotId(i, 0, (isHasNumbers) => {
                processedCount++;
                if (isHasNumbers) {
                  isEmit = true;
                }
                if (processedCount === maxSimCount && isEmit) {
                  // 所有SIM卡数据处理完毕，触发通知
                  HiLog.i(TAG, 'getNumbers onComplete emitter');
                  emitter.emit(exportEvent);
                } else if (processedCount === maxSimCount) {
                  const msg: Resource = $r('app.string.no_contact_sim_card');
                  promptAction.showToast({
                    message: msg,
                    duration: 2000
                  });
                }
              });
              HiLog.w(TAG, 'getSetupSimCardState import');
            }
          } else {
            this.simCardEmptySlot++;
            HiLog.w(TAG, 'simCardEmptySlot ' + this.simCardEmptySlot);
            processedCount++;
            if (processedCount === maxSimCount && isEmit) {
              emitter.emit(exportEvent);
            }
            if (this.simCardEmptySlot >= 2) {
              this.isShowSimEntry = false;
              HiLog.w(TAG, 'simCardEmptySlot ' + this.isShowSimEntry);
            }
          }
        }
      });
    }
  }

  @Styles
  pressedStyles() {
    .backgroundColor($r('app.color.skin_interactive_click'))
    .borderRadius($r('sys.float.corner_radius_level8'))
  }

  @Styles
  normalStyles() {
    .backgroundColor('rgba(255,255,255,0)')
  }

  build() {
    NavDestination() {
      Column() {
        List({ scroller: this.scroller }) {
          ForEach(this.itemGroupArrays, (group: LooseObject, index: number) => {
            SubHeader({
              secondaryTitle: group.headerTitle,
              secondaryTitleModifier: this.isThemeActive ?
              new TextModifier().fontColor($r('app.color.skin_font_secondary')) : undefined,
              contentMargin: {
                start: this.isTabletLandscape ? LengthMetrics.vp(16)
                  : LengthMetrics.resource($r('sys.float.margin_left'))
              }
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/settings/ImportAndExport.ets
--- a/entry/src/main/ets/pages/contacts/settings/ImportAndExport.ets
+++ b/entry/src/main/ets/pages/contacts/settings/ImportAndExport.ets
@@ -737,24 +737,35 @@
   }
 
   build() {
+    // Cache state variables before loop to avoid frequent reads
+    const isThemeActive = this.isThemeActive;
+    const isTabletLandscape = this.isTabletLandscape;
+    const curBp = this.curBp;
+    const isPC = this.isPC;
+    const isShowSimEntry = this.isShowSimEntry;
+    const fontSizeScale = this.fontSizeScale;
+    const spaceLR = this.spaceLR;
+    const itemGroupIds = this.itemGroupIds;
+    const simFlag = this.simFlag;
+
     NavDestination() {
       Column() {
         List({ scroller: this.scroller }) {
           ForEach(this.itemGroupArrays, (group: LooseObject, index: number) => {
             SubHeader({
               secondaryTitle: group.headerTitle,
-              secondaryTitleModifier: this.isThemeActive ?
+              secondaryTitleModifier: isThemeActive ?
               new TextModifier().fontColor($r('app.color.skin_font_secondary')) : undefined,
               contentMargin: {
-                start: this.isTabletLandscape ? LengthMetrics.vp(16)
+                start: isTabletLandscape ? LengthMetrics.vp(16)
                   : LengthMetrics.resource($r('sys.float.margin_left'))
               }
             })
-              .margin({ left: this.curBp === 'lg' ? $r('app.float.id_card_margin_large') : 0 })
-              .height(this.isPC ? $r('app.float.id_item_height_sm') : undefined)
+              .margin({ left: curBp === 'lg' ? $r('app.float.id_card_margin_large') : 0 })
+              .height(isPC ? $r('app.float.id_item_height_sm') : undefined)
             ListItemGroup({ style: ListItemGroupStyle.CARD }) {
               ForEach(group.items, (cardItem: LooseObject) => {
-                if (cardItem.index == 0 ? this.isShowSimEntry : true) {
+                if (cardItem.index == 0 ? isShowSimEntry : true) {
                   ListItem() {
                     Row() {
                       Column() {
@@ -774,7 +785,7 @@
                       }
                       .width(`calc(100% - 20vp)`)
                       .constraintSize({
-                        minHeight: this.isPC ? $r('app.float.id_item_height_large') :
+                        minHeight: isPC ? $r('app.float.id_item_height_large') :
                         $r('app.float.id_item_height_max')
                       })
                       .alignItems(HorizontalAlign.Start)
@@ -792,7 +803,7 @@
                     .justifyContent(FlexAlign.SpaceBetween)
                     .alignItems(VerticalAlign.Center)
                     .constraintSize({
-                      minHeight: this.isPC ? $r('app.float.id_item_height_large') :
+                      minHeight: isPC ? $r('app.float.id_item_height_large') :
                         cardItem.subTitle !== undefined ? $r('app.float.id_item_height_max')
                         : $r('app.float.id_item_height_mid')
                     })
@@ -803,17 +814,17 @@
                     .padding({
                       left: $r('app.float.id_card_margin_large'),
                       right: $r('app.float.id_card_margin_large'),
-                      top: cardItem.index == 0 ? this.fontSizeScale > 3 ? $r('app.float.id_card_item_margin_top') : 0 :
-                      FontScaleState.fetchSeniorTopAndBottomSpace(this.fontSizeScale,
+                      top: cardItem.index == 0 ? fontSizeScale > 3 ? $r('app.float.id_card_item_margin_top') : 0 :
+                      FontScaleState.fetchSeniorTopAndBottomSpace(fontSizeScale,
                         0, $r('app.float.id_card_item_margin_top')),
                       bottom: cardItem.index == 0 ?
-                        this.fontSizeScale > 3 ? $r('app.float.id_card_item_margin_top') : 0 :
-                      FontScaleState.fetchSeniorTopAndBottomSpace(this.fontSizeScale,
+                        fontSizeScale > 3 ? $r('app.float.id_card_item_margin_top') : 0 :
+                      FontScaleState.fetchSeniorTopAndBottomSpace(fontSizeScale,
                         0, $r('app.float.id_card_item_margin_top'))
                     })
                     .onClick(() => {
                       if (cardItem.index === 0 && index === 0) {
-                        if (!this.simFlag) {
+                        if (!simFlag) {
                           this.getSetupSimCardState(false);
                           HiLog.w(TAG, 'click sim entry');
                         }
@@ -828,7 +839,7 @@
                       }
                     })
                   }
-                  .id(this.itemGroupIds[index])
+                  .id(itemGroupIds[index])
                   .constraintSize({
                     minHeight: cardItem.subTitle !== undefined ? $r('app.float.id_item_height_max')
                       : $r('app.float.id_item_height_mid')
@@ -836,10 +847,10 @@
                 }
               }, (item: LooseObject) => JSON.stringify(item))
             }
-            .borderRadius(this.isPC ? $r('sys.float.corner_radius_level8') :
+            .borderRadius(isPC ? $r('sys.float.corner_radius_level8') :
             $r('sys.float.corner_radius_level10'))
             .backgroundColor($r('app.color.skin_ohos_id_color_card_bg'))
-            .margin({ left: this.spaceLR, right: this.spaceLR })
+            .margin({ left: spaceLR, right: spaceLR })
             .divider({
               strokeWidth: '1px',
               color: $r('app.color.skin_ohos_id_color_list_separator'),
@@ -868,8 +879,8 @@
     // }))
     .title(ResourceUtil.getStringByResource($r('app.string.Import_Export_Contacts')),
       {
-        mainTitleModifier: (this.isThemeActive ? this.mainTitleModifier : undefined),
-        paddingStart: this.isPC ? LengthMetrics.vp(16) : LengthMetrics.resource($r('sys.float.margin_left'))
+        mainTitleModifier: (isThemeActive ? this.mainTitleModifier : undefined),
+        paddingStart: isPC ? LengthMetrics.vp(16) : LengthMetrics.resource($r('sys.float.margin_left'))
       })
     .menus(this.TitleGuide())
     .onBackPressed(() => {
@@ -879,7 +890,7 @@
     .bindToScrollable([this.scroller])
     .backgroundColor($r('app.color.color_bind_sheet_background'))
     .padding({
-      bottom: this.curBp !== 'sm' ? $r('sys.float.padding_level0') : px2vp(this.fullScreenPadding.bottom as number)
+      bottom: curBp !== 'sm' ? $r('sys.float.padding_level0') : px2vp(this.fullScreenPadding.bottom as number)
     })
   }
 


```

## [7/50] ID: OH_0071 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export default struct DetailInfoRemarks {
  @Link mPresenter: DetailPresenter;
  @Link selectSimBuilder: SelectDialogBuilder;
  @Link maximum: number;
  @Prop telephoneTotal: number;
  @Prop meettingTotal: number;
  @Prop otherTotal: number;
  @Link moreOptionsFlag: boolean;
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;

  isEmptyDetailInfoRemarks(): boolean {
    return (
      !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.emails) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.aims) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.houses) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.websites) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.relationships) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.events)
    )
  }

  // 处理展开更多与未展开更多情况下分割线的显示
  isDividerShow(totalCount: number, index: number): Visibility {
    if (this.moreOptionsFlag) {
      if (totalCount - 1 !== index) {
        return Visibility.Visible
      } else {
        return Visibility.None
      }
    } else {
      if (this.telephoneTotal + this.meettingTotal + index + 1 < this.maximum && totalCount - 1 === index) {
        return Visibility.None
      } else if (this.telephoneTotal + this.meettingTotal + index + 1 < this.maximum && totalCount - 1 !== index) {
        return Visibility.Visible
      } else {
        return Visibility.None
      }
    }
  }

  isItemShow(index: number): Visibility {
    let isVisibility: Visibility = Visibility.None;
    if (this.moreOptionsFlag) {
      isVisibility = Visibility.Visible
    } else {
      if (this.telephoneTotal + this.meettingTotal + index < this.maximum) {
        isVisibility = Visibility.Visible
      } else {
        isVisibility = Visibility.None
      }
    }
    return isVisibility
  }

  build() {
    Column() {
      List() {
        if (this.isEmptyDetailInfoRemarks()) {
          LazyForEach(this.mPresenter.detailInfoRemarksSources, (item: ContactStrInterface, index: number) => {
            if (JSON.parse(item.data).data) {
              ListItem() {
                Column() {
                  DetailInfoListItem({
                    listItem: JSON.parse(item.data),
                    mPresenter: $mPresenter,
                    hasArrow: false,
                  });
                  Divider()
                    .color($r('app.color.skin_ohos_id_color_list_separator'))
                    .strokeWidth('1px')
                    .width('100%')
                    .visibility(this.isDividerShow(this.mPresenter.detailInfoRemarksSources.totalCount(), index))
                    .padding({ left: $r('sys.float.padding_level4'), right: $r('sys.float.padding_level4'), })
                }
              }
              .visibility(this.isItemShow(index))
            }
          }, (item: ContactStrInterface, index: number) => JSON.stringify(item) + JSON.stringify(index))
        }
      }
      .scrollBar(BarState.Off)
      .edgeEffect(EdgeEffect.None)
    }
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets
--- a/entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets
+++ b/entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets
@@ -41,6 +41,7 @@
 const TAG = 'DetailInfoRemarks';
 const DETAILS_PRESS_CHOOSE_EVENT = 'DETAILS_PRESS_CHOOSE_EVENT';
 
+@Reusable
 @Component
 export default struct DetailInfoRemarks {
   @Link mPresenter: DetailPresenter;


```

## [8/50] ID: OH_0338 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-func-as-arg-for-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `HMRouterExamples/features/custom_template_cases/src/main/ets/ezLongTake/CardLongTakePageOne.ets`
- **Warning:** Do not use functions as input parameters for creating reusable components

### Buggy Snippet
```typescript
@Component
export struct CardLongTakePageOne {
  @State dataSource: WaterFlowDataSource = new WaterFlowDataSource();
  @State columnWidth: number = 0;
  @State columnType: string = '';
  @StorageProp('currentBreakpoint') @Watch('upDateColumnData') currentBreakpoint: string = '';

  aboutToAppear(): void {
    for (let i = 0; i < 100; i++) {
      this.dataSource.pushData(new CardAttr());
    }
    this.upDateColumnData();
  }

  build() {
    Stack() {
      WaterFlow() {
        LazyForEach(this.dataSource, (item: CardAttr, index: number) => {
          FlowItem() {
            CardComponent({
              indexValue: index.toString(),
              cardAttr: item,
              onColumnClicked: (_index: string) => {
                const animator =
                  HMRouterTransitions.cardLongTake(Constants.getFlowItemIdByIndex(_index), 'test', {
                    onTransitionStart: () => {
                      Logger.info('onTransitionStart');
                    },
                    onTransitionEnd: () => {
                      Logger.info('onTransitionEnd');
                    }
                  });
                HMRouterMgr.pushAsync({
                  pageUrl: PageRouteConstants.CARD_LONG_TAKE_PAGE_TWO,
                  param: _index,
                  animator: animator
                });
              }
            });
          }
          .borderRadius(9)
          .width('100%')
          .clip(true)
          .id(Constants.getFlowItemIdByIndex(index.toString()));
        }, (item: CardAttr, index: number) => index.toString());
      }
      .cachedCount(4)
      .columnsTemplate(this.columnType)
      .columnsGap(5)
      .rowsGap(5)
      .width('100%')
      .height('100%');
    }.size({
      width: '100%',
      height: '100%'
    })
    .padding({
      left: 10,
      right: 10
    });
  }

  private upDateColumnData(): void {
    let currentBreakpoint: string | undefined = AppStorage.get('currentBreakpoint');
    if (currentBreakpoint === 'xs' || currentBreakpoint === 'sm') {
      this.columnType = '1fr 1fr';
    } else if (currentBreakpoint === 'md') {
      this.columnType = '1fr 1fr 1fr';
    } else {
      this.columnType = '1fr 1fr 1fr 1fr';
    }
  }
}
```

### Patch
```diff
// File: HMRouterExamples/features/custom_template_cases/src/main/ets/ezLongTake/CardLongTakePageOne.ets
--- a/HMRouterExamples/features/custom_template_cases/src/main/ets/ezLongTake/CardLongTakePageOne.ets
+++ b/HMRouterExamples/features/custom_template_cases/src/main/ets/ezLongTake/CardLongTakePageOne.ets
@@ -36,6 +36,23 @@
     this.upDateColumnData();
   }
 
+  private handleColumnClick(_index: string): void {
+    const animator =
+      HMRouterTransitions.cardLongTake(Constants.getFlowItemIdByIndex(_index), 'test', {
+        onTransitionStart: () => {
+          Logger.info('onTransitionStart');
+        },
+        onTransitionEnd: () => {
+          Logger.info('onTransitionEnd');
+        }
+      });
+    HMRouterMgr.pushAsync({
+      pageUrl: PageRouteConstants.CARD_LONG_TAKE_PAGE_TWO,
+      param: _index,
+      animator: animator
+    });
+  }
+
   build() {
     Stack() {
       WaterFlow() {
@@ -44,22 +61,7 @@
             CardComponent({
               indexValue: index.toString(),
               cardAttr: item,
-              onColumnClicked: (_index: string) => {
-                const animator =
-                  HMRouterTransitions.cardLongTake(Constants.getFlowItemIdByIndex(_index), 'test', {
-                    onTransitionStart: () => {
-                      Logger.info('onTransitionStart');
-                    },
-                    onTransitionEnd: () => {
-                      Logger.info('onTransitionEnd');
-                    }
-                  });
-                HMRouterMgr.pushAsync({
-                  pageUrl: PageRouteConstants.CARD_LONG_TAKE_PAGE_TWO,
-                  param: _index,
-                  animator: animator
-                });
-              }
+              onColumnClicked: this.handleColumnClick
             });
           }
           .borderRadius(9)


```

## [9/50] ID: OH_0060 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/contacts/search/ContactSearch.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
ListItem() {
                Stack({ alignContent: Alignment.BottomEnd }) {
                  Row() {
                    SearchPhotoView({ item: item, presenter: this.presenter })
                    Column() {
                      ContactSearchInfo({
                        name: item.contact.name.replace(hasComma, COMMA_REPLACE).split(labelMatch),
                        organization: item.contact.organization.replace(hasComma, COMMA_REPLACE).split(labelMatch),
                        phoneNumbers: item.contact.phoneNumbers,
                        inputKeyword: this.presenter.inputKeyword,
                        positions: item.contact.position.replace(hasComma, COMMA_REPLACE).split(labelMatch),
                        emails: this.presenter.processData(item.contact.emails),
                        imInfo: this.presenter.processData(item.contact.imInfo),
                        familyAddress: this.presenter.processData(item.contact.familyAddress),
                        note: item.contact.note.replace(hasComma, COMMA_REPLACE).split(labelMatch),
                        nickname: item.contact.nickname.replace(hasComma, COMMA_REPLACE).split(labelMatch),
                        nameHasHighlightLabel: item.contact.name.includes('em'),
                        organizationRemoveHighlightLabel:
                        item.contact.organization.replace(new RegExp('<\/?.+?>', 'g'), ''),
                        positionRemoveHighlightLabel:
                        item.contact.position.replace(new RegExp('<\/?.+?>', 'g'), ''),
                        nameIsEmpty: StringUtil.isEmpty(item.contact.name)
                      })
                    }
                    .flexShrink(1)
                    .alignItems(HorizontalAlign.Start)
                    .margin({
                      start: this.isPC ? LengthMetrics.vp(0) :
                      LengthMetrics.resource($r('app.float.id_card_margin_xxl'))
                      })
                  }
                  .alignItems(VerticalAlign.Center)
                  .width('100%')
                  .constraintSize({
                    minHeight: this.isPC ? $r('app.float.id_item_height_large') :
                    $r('app.float.id_item_height_max')
                  })
                }
              }
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/search/ContactSearch.ets
--- a/entry/src/main/ets/pages/contacts/search/ContactSearch.ets
+++ b/entry/src/main/ets/pages/contacts/search/ContactSearch.ets
@@ -812,6 +812,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct SearchPhotoView {
   @Link presenter: ContactListPresenter;
@@ -893,6 +894,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct ContactSearchInfo {
   @State name: string[] = [];
@@ -1187,6 +1189,7 @@
   }
 }
 
+@Reusable
 @Component
 struct FormatNumberText {
   private phoneNumber: string = '';


```

## [10/50] ID: OH_0268 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-local-var-to-replace-state-var`
- **Result:** `LINTER_FAIL`
- **Target File:** `product/phone/src/main/ets/pages/biometricsandpassword/module/privacyPassword/component/MixAndNumberPasswordPageButton.ets`
- **Warning:** Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
@Component
export default struct MixAndNumberPasswordPageButton {
  @Prop resourceLeft: Resource;
  @Prop resourceRight: Resource;
  @Prop buttonAreaWidth: number;
  @Prop enableClick: boolean;
  @State bottomMargin: number = 16;
  private navigationIndicatorHeight: number = 48;
  @State isHeightTooSmall: boolean = false;
  @Consume @Watch('onContainerChange') containerHeight: number;

  onContainerChange() {
    this.isHeightTooSmall = this.containerHeight < LARGE_LIMIT_HEIGHT;
  }
  cancelClicked: () => void = () => {
  };

  continueClicked: () => void = () => {
  };

  aboutToAppear(): void {
    try {
      this.bottomMargin = getContext().resourceManager.getNumber($r('sys.float.padding_level8'));
      this.bottomMargin = this.navigationIndicatorHeight + this.bottomMargin;
    } catch (err) {
      this.bottomMargin = 16;
      Log.error(TAG, `getBottomMargin error, error code: ${err?.code}, message: ${err?.message}.`);
    }
  }

  build() {
   if (FontScaleUtils.buttonColumnLayout(this.buttonAreaWidth, this.resourceLeft, this.resourceRight)) {
     if (this.isHeightTooSmall && FontScaleUtils.isExtraLargeFontMode(getContext() as common.UIAbilityContext)) {
       Column({ space: 12 }) {
         Button(this.resourceLeft)
           .fontColor($r('sys.color.font_emphasize'))
           .fontWeight(FontWeight.Medium)
           .buttonStyle(ButtonStyleMode.NORMAL)
           .type(ButtonType.Normal)
           .borderRadius($r('sys.float.corner_radius_level10'))
           .width('100%')
           .fontSize(FontScaleUtils.getRealPX(getContext(), $r('sys.float.ohos_id_text_size_button1')))
           .onClick(() => {
             this.cancelClicked();
           })
         Button(this.resourceRight)
           .fontColor($r('sys.color.font_emphasize'))
           .fontWeight(FontWeight.Medium)
           .buttonStyle(ButtonStyleMode.NORMAL)
           .type(ButtonType.Normal)
           .borderRadius($r('sys.float.corner_radius_level10'))
           .width('100%')
           .enabled(this.enableClick)
           .fontSize(FontScaleUtils.getRealPX(getContext(), $r('sys.float.ohos_id_text_size_button1')))
           .onClick(() => {
             this.continueClicked();
           })
       }
       .width(this.buttonAreaWidth)
       .margin({
         top: $r('sys.float.padding_level8'),
         bottom: $r('sys.float.padding_level8')
       })
       .flexShrink(0)
     } else {
       Column({ space: 12 }) {
         Button(this.resourceLeft)
           .buttonCommonStyle()
           .width('100%')
           .onClick(() => {
             this.cancelClicked();
           })
         Button(this.resourceRight)
           .buttonCommonStyle()
           .width('100%')
           .enabled(this.enableClick)
           .onClick(() => {
             this.continueClicked();
           })
       }
       .width(this.buttonAreaWidth)
       .margin({
         top: $r('sys.float.padding_level8'),
         bottom: $r('sys.float.padding_level8')
       })
       .flexShrink(0)
     }
    } else {
      Row({ space: 12 }) {
        Button(this.resourceLeft)
          .buttonCommonStyle()
          .layoutWeight(1)
          .onClick(() => {
            this.cancelClicked();
          })
        Button(this.resourceRight)
          .buttonCommonStyle()
          .layoutWeight(1)
          .enabled(this.enableClick)
          .onClick(() => {
            this.continueClicked();
          })
      }
      .flexShrink(0)
      .constraintSize({
        minHeight: $r('app.float.wh_40'),
        maxWidth: CommonConstants.MAX_BUTTON_WIDTH,
      })
      .justifyContent(FlexAlign.Center)
      .margin({
        top: $r('sys.float.padding_level8'),
        bottom: $r('sys.float.padding_level8')
      })
    }
  }
}
```

### Patch
```diff
// File: product/phone/src/main/ets/pages/biometricsandpassword/module/privacyPassword/component/MixAndNumberPasswordPageButton.ets
--- a/product/phone/src/main/ets/pages/biometricsandpassword/module/privacyPassword/component/MixAndNumberPasswordPageButton.ets
+++ b/product/phone/src/main/ets/pages/biometricsandpassword/module/privacyPassword/component/MixAndNumberPasswordPageButton.ets
@@ -29,12 +29,8 @@
   @Prop enableClick: boolean;
   @State bottomMargin: number = 16;
   private navigationIndicatorHeight: number = 48;
-  @State isHeightTooSmall: boolean = false;
-  @Consume @Watch('onContainerChange') containerHeight: number;
+  @Consume containerHeight: number;
 
-  onContainerChange() {
-    this.isHeightTooSmall = this.containerHeight < LARGE_LIMIT_HEIGHT;
-  }
   cancelClicked: () => void = () => {
   };
 
@@ -52,8 +48,9 @@
   }
 
   build() {
+   const isHeightTooSmall = this.containerHeight < LARGE_LIMIT_HEIGHT;
    if (FontScaleUtils.buttonColumnLayout(this.buttonAreaWidth, this.resourceLeft, this.resourceRight)) {
-     if (this.isHeightTooSmall && FontScaleUtils.isExtraLargeFontMode(getContext() as common.UIAbilityContext)) {
+     if (isHeightTooSmall && FontScaleUtils.isExtraLargeFontMode(getContext() as common.UIAbilityContext)) {
        Column({ space: 12 }) {
          Button(this.resourceLeft)
            .fontColor($r('sys.color.font_emphasize'))


```

## [11/50] ID: OH_0018 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

### Buggy Snippet
```typescript
@Component
struct ContactsList {
  @Link presenter: BatchSelectContactsPresenter;

  build() {
    Column() {
      List({ initialIndex: this.presenter.initialIndex }) {
        LazyForEach(this.presenter.contactsSource, (item, index) => {

          ListItem() {
            Stack({ alignContent: Alignment.BottomEnd }) {
              Column() {
                if (item.showIndex) {
                  Flex({ direction: FlexDirection.Column,
                    justifyContent: FlexAlign.End,
                    alignItems: ItemAlign.Start }) {
                    Text(item.contact.namePrefix)
                      .fontColor($r("sys.color.ohos_fa_text_secondary"))
                      .fontSize($r("sys.float.ohos_id_text_size_sub_title3"))
                      .fontWeight(FontWeight.Medium)
                      .textAlign(TextAlign.Start)
                  }
                  .padding({ left: $r("app.float.id_card_margin_max"), bottom: $r("app.float.id_card_margin_large") })
                  .width('100%')
                  .height($r("app.float.id_item_height_mid"))
                }

                BatchSelectContactItemView({
                  item: item.contact,
                  index: item.index,
                  onContactItemClicked: (index, indexChild) => this.presenter.onContactItemClicked(index, indexChild),
                  showIndex: item.showIndex,
                  showDivifer: item.showDivifer
                })
              }

              if (item.showDivifer) {
                Divider()
                  .color($r("sys.color.ohos_id_color_list_separator"))
                  .margin({ left: 76, right: $r("app.float.id_card_margin_max") })
              }
            }
          }
        }, (item) => item.contact.contactId.toString())
      }
      .width('100%')
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring)
      .onScrollIndex((firstIndex: number, lastIndex: number) => {
        this.presenter.resetInitialIndex(firstIndex);
      })
    }
    .width('100%')
    .padding({ top: $r("app.float.id_card_margin_mid"), bottom: $r("app.float.id_card_margin_mid") })
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
--- a/entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
+++ b/entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
@@ -220,6 +220,7 @@
       .width('100%')
       .listDirection(Axis.Vertical)
       .edgeEffect(EdgeEffect.Spring)
+      .cachedCount(5)
     }
     .width('100%')
     .backgroundColor(Color.White)
@@ -276,6 +277,7 @@
       .width('100%')
       .listDirection(Axis.Vertical)
       .edgeEffect(EdgeEffect.Spring)
+      .cachedCount(5)
       .onScrollIndex((firstIndex: number, lastIndex: number) => {
         this.presenter.resetInitialIndex(firstIndex);
       })


```

## [12/50] ID: OH_0017 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct RecentList {
  @Link presenter: BatchSelectContactsPresenter;

  build() {
    Column() {
      List({ space: 0, initialIndex: 0 }) {
        LazyForEach(this.presenter.recentSource, (item, index: number) => {
          ListItem() {
            Stack({ alignContent: Alignment.BottomEnd }) {
              BatchSelectRecentItemView({
                item: item.calllog,
                index: item.index,
                onRecentItemClicked: (index) => this.presenter.onRecentItemClicked(index)
              })

              if (item.showDivifer) {
                Divider()
                  .color($r("sys.color.ohos_id_color_list_separator"))
                  .margin({ left: 76, right: $r("app.float.id_card_margin_max") })
              }
            }
          }
        }, (item) => item.calllog.id.toString())
      }
      .width('100%')
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring)
    }
    .width('100%')
    .backgroundColor(Color.White)
    .padding({ top: $r("app.float.id_card_margin_mid"), bottom: $r("app.float.id_card_margin_mid") })
    .borderRadius($r("sys.float.ohos_id_corner_radius_card"))
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
--- a/entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
+++ b/entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
@@ -192,6 +192,7 @@
   }
 }
 
+@Reusable
 @Component
 struct RecentList {
   @Link presenter: BatchSelectContactsPresenter;
@@ -228,6 +229,7 @@
   }
 }
 
+@Reusable
 @Component
 struct ContactsList {
   @Link presenter: BatchSelectContactsPresenter;
@@ -285,6 +287,7 @@
   }
 }
 
+@Reusable
 @Component
 struct NoContactsEmptyView {
   @State presenter: BatchSelectContactsPresenter = BatchSelectContactsPresenter.getInstance();


```

## [13/50] ID: OH_0063 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-func-as-arg-for-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets`
- **Warning:** Do not use functions as input parameters for creating reusable components

### Buggy Snippet
```typescript
@Component
struct ContactsList {
  @Link presenter: ContactsPickerPresenter;
  @Link isShowLearnMore: boolean
  private scroller: Scroller = new Scroller();
  @State alphabetSelected: number = 0;
  @State isAlphabetClicked: boolean = false;
  @State dragList: boolean = false;
  @State alphabetIndexPresenter: AlphabetIndexerPresenter = this.presenter.alphabetIndexPresenter;
  @StorageLink('isShowSmartWindow') isShowSmartWindow: boolean = false;
  @StorageLink('speedDialContact') speedDialContact: string = '';
  @State pageType: string = 'contactsListPage';
  @StorageLink('spaceLR') spaceLR: Resource = $r('sys.float.padding_level8');
  isContactMultiSelect: boolean = true;
  // lastFirstIndex
  private lastFirstIndex: number = -1;
  // lastLastIndex
  private lastLastIndex: number = -1;
  @StorageProp('splitStatus') splitStatus: SplitStatus = SplitStatus.DEFAULT;
  @Prop selectedCount: number = 0;
  @Prop selectedViewShow: boolean;
  @Prop isDisplayByName: boolean;
  @Prop userId: number;
  @Prop localId: number;
  @Prop verdeSecurityShieldHeight: number
  @Prop isSaveExistContact: boolean;
  @Link @Watch('alertOnChange') isShowOnlyAccessedAlert: boolean;
  @State preListItemNum: number = 1;
  @State deleteContact: boolean = false;
  // 是否启动无障碍
  @StorageProp(AccessibilityUtil.ISOPENACCESSIBILITY) isOpenAccessibility: boolean = false;
  private isPC: boolean = EnvironmentProp.isPC();
  @StorageProp('isVerde') isVerde: boolean = false;
  private slidingMultipleSelectionsUtil: SlidingMultipleSelectionsUtil =
    new SlidingMultipleSelectionsUtil(this.scroller, 56);


  aboutToAppear(): void {
    HiLog.w(TAG, 'aboutToAppear123');
    this.alertOnChange();
    this.slidingMultipleSelectionsUtil.isSliding = this.isContactMultiSelect;
  }

  alertOnChange() {
    if (this.isShowOnlyAccessedAlert) {
      this.preListItemNum = 2;
    } else {
      this.preListItemNum = 1;
    }
  }

  build() {
    Stack({ alignContent: Alignment.TopEnd }) { //右侧字母排序位置
      List({ initialIndex: 0, scroller: this.scroller }) {
        if (this.isShowOnlyAccessedAlert && !this.isVerde) {
          ListItem() {
            SecureAccessPopupTip({
              isShowOnlyAccessedAlert: this.isShowOnlyAccessedAlert,
              isShowLearnMore: this.isShowLearnMore
            });
          }
        }

        ListItem() {
          Row() {
            Text($r('app.string.all_contacts2'))
              .fontSize($r('sys.float.Body_M'))
              .fontWeight(FontWeight.Medium)
              .fontColor($r('app.color.skin_font_secondary'))
              .layoutWeight(1)
              .textAlign(TextAlign.Start)
              .maxFontScale(pickerMaxFontScale)

            if (this.isContactMultiSelect) {
              Text(this.presenter.allSelectMessage)
                .id('all_select_message')
                .fontSize($r('sys.float.Body_M'))
                .fontWeight(FontWeight.Medium)
                .fontColor($r('app.color.skin_font_emphasize'))
                .width('30%')
                .textAlign(TextAlign.End)
                .maxFontScale(pickerMaxFontScale)
                .accessibilityRole(AccessibilityRoleType.BUTTON)
                .layoutWeight(1)
                .onClick(() => {
                  this.presenter.selectAllOnClick();
                })
            }
          }
          .visibility((this.splitStatus === SplitStatus.ONE_THREE_SPLIT ) ||
            (this.splitStatus === SplitStatus.HALF_SPLIT) ? Visibility.None : Visibility.Visible)
          .width('100%')
          .constraintSize({
            minHeight: this.isPC ? $r('app.float.id_item_height_sm') : 56
          })
          .padding({
            left: this.isPC ? $r('sys.float.padding_level12') : this.mirrorLanguageCheck(),
            top: $r('sys.float.padding_level4'),
            right: $r('sys.float.padding_level16'),
          })
          .enabled(!this.selectedViewShow)
        }

        LazyForEach(this.presenter.favoriteSource, (item: ContactPickerListItem, index: number) => {
          ListItem() {
            ContactsPickerListItem({
              presenter: this.presenter,
              userId: this.userId,
              localId: this.localId,
              item: item,
              index: index,
              isMultiSelect: this.isContactMultiSelect,
              isDisplayByName: this.isDisplayByName,
              isSaveExistContact: this.isSaveExistContact,
              maxFontScale: pickerMaxFontScale,
              customIndexTitle: $r('app.string.favorite'),
            })
          }
        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))

        //遍历位置
        LazyForEach(this.presenter.contactsSource, (item: ContactPickerListItem, index: number) => {
          ListItem() {
            ContactsPickerListItem({
              presenter: this.presenter,
              userId: this.userId,
              localId: this.localId,
              item: item,
              index: index,
              isMultiSelect: this.isContactMultiSelect,
              isDisplayByName: this.isDisplayByName,
              isSaveExistContact: this.isSaveExistContact,
              maxFontScale: pickerMaxFontScale,
            })
          }
        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
      }
      .accessibilityLevel('no')
      .width('100%')
      .height('100%')
      .contentEndOffset(this.isVerde ? this.verdeSecurityShieldHeight : 0)
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
      .scrollBar(BarState.Off)
      .onScrollIndex((firstIndex: number, lastIndex: number) => {
        this.slidingMultipleSelectionsUtil.scrollStartIndex = firstIndex;
        this.slidingMultipleSelectionsUtil.scrollEndIndex = lastIndex;

        if (firstIndex === this.lastFirstIndex && lastIndex === this.lastLastIndex) {
          return
        }
        this.lastFirstIndex = firstIndex;
        this.lastLastIndex = lastIndex;
        const contactFirstIndex = firstIndex <= this.preListItemNum ? 0 : firstIndex - this.preListItemNum;
        const contactLastIndex = lastIndex <= this.preListItemNum ? 0 : lastIndex - this.preListItemNum;
        let curIndex = this.alphabetIndexPresenter.getAlphabetSelected(contactFirstIndex);
        if (this.alphabetSelected !== curIndex) {
          this.alphabetSelected = curIndex;
        }
      })
      .onScrollStart(() => {
        emitter.emit(AlphabetIndexerPage.innerEvent);
        this.dragList = true;
        this.isAlphabetClicked = false;
      })
      .onScrollStop(() => {
        this.isAlphabetClicked = true;
        this.dragList = false;
      })
      .nestedScroll({
        scrollForward: NestedScrollMode.PARALLEL,
        scrollBackward: NestedScrollMode.PARALLEL
      })
      .gesture(PanGesture({ direction: PanDirection.Vertical })
        .onActionStart((event: GestureEvent) => {
          for (let i = 0; i < this.preListItemNum; ++i) {
            this.slidingMultipleSelectionsUtil.oldSelectStatus[i] = false;
            this.slidingMultipleSelectionsUtil.curSelectStatus[i] = false;
          }

          for (let i = 0; i < this.presenter.favoriteSource.totalCount(); ++i) {
            let index = i + this.preListItemNum;
            let item = this.presenter.favoriteSource.getData(i);
            let selectStatus = this.presenter.selectedContactsMap.get(item?.contactId)?.has(
              item?.pickerShowSubData.keyValue) ?? false;
            this.slidingMultipleSelectionsUtil.oldSelectStatus[index] = selectStatus;
            this.slidingMultipleSelectionsUtil.curSelectStatus[index] = selectStatus;
          }

          for (let i = 0; i < this.presenter.contactsSource.totalCount(); ++i) {
            let index = i + this.preListItemNum + this.presenter.favoriteSource.totalCount();
            let item = this.presenter.contactsSource.getData(i);
            let selectStatus = this.presenter.selectedContactsMap.get(item?.contactId)?.has(
              item?.pickerShowSubData.keyValue) ?? false;
            this.slidingMultipleSelectionsUtil.oldSelectStatus[index] = selectStatus;
            this.slidingMultipleSelectionsUtil.curSelectStatus[index] = selectStatus;
          }

          this.slidingMultipleSelectionsUtil.onActionStart(event.fingerList[0]);
        })
        .onActionUpdate((event: GestureEvent) => {
          if (this.selectedCount >= this.presenter.selectLimit) {
            this.slidingMultipleSelectionsUtil.isStopScroll = true;
            this.slidingMultipleSelectionsUtil.stopScroll();
          } else {
            this.slidingMultipleSelectionsUtil.isStopScroll = false;
          }

          let updateIndexes = this.slidingMultipleSelectionsUtil.onActionUpdate(event.fingerList[0], (index) => {
            let curSelectStatus = false;
            if (index >= this.preListItemNum) {
              index -= this.preListItemNum;
              if (index >= this.presenter.favoriteSource.totalCount()) {
                index -= this.presenter.favoriteSource.totalCount();
                let item = this.presenter.contactsSource.getData(index);
                curSelectStatus = this.presenter.selectedContactsMap.get(item?.contactId)?.has(
                  item?.pickerShowSubData.keyValue) ?? false;
              } else {
                let item = this.presenter.favoriteSource.getData(index);
                curSelectStatus = this.presenter.selectedContactsMap.get(item?.contactId)?.has(
                  item?.pickerShowSubData.keyValue) ?? false;
              }
            }
            return curSelectStatus;
          });
          updateIndexes.forEach((index) => {
            if (index >= this.preListItemNum) {
              index -= this.preListItemNum;
              if (index >= this.presenter.favoriteSource.totalCount()) {
                index -= this.presenter.favoriteSource.totalCount();
                let item = this.presenter.contactsSource.getData(index);
                this.presenter.itemOnClick(
                  item?.contactId, item?.pickerShowSubData.keyValue, item?.pickerShowSubData.dataId);
              } else {
                let item = this.presenter.favoriteSource.getData(index);
                this.presenter.itemOnClick(
                  item?.contactId, item?.pickerShowSubData.keyValue, item?.pickerShowSubData.dataId);
              }
            }
          })
        })
        .onActionEnd(() => {
          this.slidingMultipleSelectionsUtil.onActionEnd();
        })
        .onActionCancel(() => {
          this.slidingMultipleSelectionsUtil.onActionEnd();
        }),
        GestureMask.Normal
      )
      .onGestureRecognizerJudgeBegin(
        (event: BaseGestureEvent, current: GestureRecognizer, recognizers: Array<GestureRecognizer>) => {
          return this.slidingMultipleSelectionsUtil.onGestureRecognizerJudgeBegin(event.fingerList[0], current);
        })
      .onAreaChange((oldValue: Area, newValue: Area)=>{
        this.slidingMultipleSelectionsUtil.listWidth = newValue.width as number
        this.slidingMultipleSelectionsUtil.areaY = newValue.globalPosition.y as number;
        this.slidingMultipleSelectionsUtil.contentHeight = newValue.height as number;
      })

      if (DisplaySplitUtil.isShowIndex(this.splitStatus)){
        AlphabetIndexerPage({
          scroller: this.scroller,
          needPop: !this.isVerde,
          favoriteIndexerPresenter: this.alphabetIndexPresenter,
          selected: this.alphabetSelected,
          isClicked: $isAlphabetClicked,
          isAutoCollapse: true,
          preIndexNum: this.preListItemNum,
          scrollIndexOffset: false,
          hasFavorite: true,
        })
          .id('picker_contacts_alphabetIndexer_alphabetIndexerPage')
          .width('24vp')
          .margin({
            top: $r('sys.float.padding_level8'),
            left: $r('sys.float.padding_level2'),
            right: $r('sys.float.padding_level2'),
          })
      }
    }
    .width('100%')
  }

  private mirrorLanguageCheck(): Length | undefined {
    if (i18n.System.getSystemLanguage() === 'ug' || i18n.System.getSystemLanguage() === 'ar') {
      return $r('sys.float.padding_level12');
    } else {
      return $r('sys.float.padding_level8');
    }
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets
--- a/entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets
+++ b/entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets
@@ -1811,12 +1811,14 @@
     .opacity(1)
   }
 
+  handlePixelMapCallback = (res: PixelMap | null): void => {
+    this.photoPixelMap = res;
+  }
+
   updateInfo() {
     this.checkedSet = this.presenter.selectedContactsMap.get(this.item.contactId) ?? new Set();
     getPixelMapFromFileForContactPicker(this.item.contactId.toString(), this.localId, this.userId,
-      (res: PixelMap | null) => {
-        this.photoPixelMap = res;
-      }, ContactsGlobalThisHelper.GetGlobalThis().getDefaultUIContext(), false)
+      this.handlePixelMapCallback, ContactsGlobalThisHelper.GetGlobalThis().getDefaultUIContext(), false)
   }
 
   aboutToAppear() {


```

## [14/50] ID: OH_0165 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/MainAbility/pages/index.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let i = 0; i < this.bleDeviceList.length; i++) {
            let device: BleDevice = this.bleDeviceList[i];
            if (!BleManager.getInstance().isConnected(device)) {
                ArrayHelper.removeIndex(this.bleDeviceList, i);
            }
        }
```

### Patch
```diff
// File: entry/src/main/ets/MainAbility/pages/index.ets
--- a/entry/src/main/ets/MainAbility/pages/index.ets
+++ b/entry/src/main/ets/MainAbility/pages/index.ets
@@ -68,6 +68,7 @@
     }
 
     build() {
+        const connectedDevicesCache = this.connectedDevices;
         Column() {
             Column() {
                 Text($r('app.string.scan_setting')).fontSize(14).fontColor($r('app.color.colorPrimary')).margin({bottom:10})
@@ -125,7 +126,7 @@
                 ForEach(this.bleDeviceList, (device: BleDevice) => {
                     ListItem() {
                         Row() {
-                            if (this.isConnected(device)) {
+                            if (ArrayHelper.contains(connectedDevicesCache, device.getMac())) {
                                 Image($r('app.media.ic_blue_connected')).objectFit(ImageFit.None).width(30).height(30)
                                 Column(){
                                     Text(device.getName()).margin({bottom:2}).fontSize(14).fontColor($r('app.color.colorPrimary'))


```

## [15/50] ID: OH_0169 | ArkTS （F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
this.allBundleInfo.forEach(bundleInfo => {
        if (bundleInfo.bundleName === bundleNames[i]) {
          this.applicationList.push(
            new ApplicationObj(
              bundleInfo.label,
              bundleInfo.icon,
              i,
              bundleInfo.tokenId,
              this.list[0].permission,
              bundleInfo.zhTag,
              bundleInfo.indexTag,
              bundleInfo.language,
              bundleInfo.bundleName) // Get the first letter in the returned initials array
          );
          this.isRisk[i] = false;
          try {
            atManager.getPermissionFlags(bundleInfo.tokenId, this.list[0].permission).then(data => {
              if (data == Constants.PERMISSION_POLICY_FIXED) {
                this.isRisk[i] = true;
              }
            })
          }
          catch(err) {
            console.log(TAG + 'getPermissionFlags error: ' + JSON.stringify(err));
          }
          // 0: have permission; -1: no permission
          let boole = true;
          this.permissionNum++;
          for (let j = 0; j < this.list.length; j++) {
            if (bundleInfo.permissions.indexOf(this.list[j].permission) == -1) {
              continue;
            }
            verifyAccessToken(bundleInfo.tokenId, this.list[j].permission).then((access) => {
              if (Number(access) === Constants.PERMISSION_INDEX) {
                if (boole) {
                  this.toggleIsOn[i] = true;
                }
              } else {
                if (boole) {
                  this.permissionNum--;
                }
                boole = false;
                this.toggleIsOn[i] = false;
              }
            });
          }
        }
      })
```

### Patch
```diff
// File: permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
--- a/permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
+++ b/permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
@@ -95,17 +95,20 @@
           res.reqPermissionDetails.forEach(item => {
             reqPermissions.push(item.name);
           })
-          for (let j = 0; j < this.list.length; j++) {
-            if ((this.list[j].permission == PRECISE_LOCATION_PERMISSION) && (res.targetVersion >= Constants.API_VERSION_SUPPORT_STAGE)) {
+          const listCache = this.list;
+          const listLength = listCache.length;
+          for (let j = 0; j < listLength; j++) {
+            const currentPermission = listCache[j].permission;
+            if ((currentPermission == PRECISE_LOCATION_PERMISSION) && (res.targetVersion >= Constants.API_VERSION_SUPPORT_STAGE)) {
               continue;
             }
-            if ((this.list[j].permission == FUZZY_LOCATION_PERMISSION) && (res.targetVersion < Constants.API_VERSION_SUPPORT_STAGE)) {
+            if ((currentPermission == FUZZY_LOCATION_PERMISSION) && (res.targetVersion < Constants.API_VERSION_SUPPORT_STAGE)) {
               continue;
             }
-            if (reqPermissions.indexOf(this.list[j].permission) == -1) {
+            if (reqPermissions.indexOf(currentPermission) == -1) {
               continue;
             }
-            verifyAccessToken(res.appInfo.accessTokenId, this.list[j].permission).then((access) => {
+            verifyAccessToken(res.appInfo.accessTokenId, currentPermission).then((access) => {
               if (Number(access) === abilityAccessCtrl.GrantStatus.PERMISSION_DENIED) {
                 this.polymorphismIsOn[index] = false;
               }
@@ -357,11 +360,14 @@
           // 0: have permission; -1: no permission
           let boole = true;
           this.permissionNum++;
-          for (let j = 0; j < this.list.length; j++) {
-            if (bundleInfo.permissions.indexOf(this.list[j].permission) == -1) {
+          const listCache = this.list;
+          const listLength = listCache.length;
+          for (let j = 0; j < listLength; j++) {
+            const currentPermission = listCache[j].permission;
+            if (bundleInfo.permissions.indexOf(currentPermission) == -1) {
               continue;
             }
-            verifyAccessToken(bundleInfo.tokenId, this.list[j].permission).then((access) => {
+            verifyAccessToken(bundleInfo.tokenId, currentPermission).then((access) => {
               if (Number(access) === Constants.PERMISSION_INDEX) {
                 if (boole) {
                   this.toggleIsOn[i] = true;


```

## [16/50] ID: OH_0301 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/encryptionProtection.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let j in globalThis.sandbox2linkFile[key]) {
            if (globalThis.sandbox2linkFile[key][j][2] == this.linkFileName) {
              let linkFile = globalThis.sandbox2linkFile[key][j];
              this.dlpFile = linkFile[1]
              this.srcFd = linkFile[3]
              this.showData(this.dlpFile.dlpProperty);
              this.isDlpFile = true;
              return
            }
          }
```

### Patch
```diff
// File: entry/src/main/ets/pages/encryptionProtection.ets
--- a/entry/src/main/ets/pages/encryptionProtection.ets
+++ b/entry/src/main/ets/pages/encryptionProtection.ets
@@ -294,12 +294,13 @@
       }
       // foreach
       property.authUsers = []
+      const accountType = this.domainOrCloudAccount;
       this.staffDataArrayReadOnly && this.staffDataArrayReadOnly.forEach(item => {
         property.authUsers.push({
           authAccount: item.authAccount,
           authPerm: dlpPermission.AuthPermType.READ_ONLY,
           permExpiryTime: Date.UTC(2025, 1, 1),
-          authAccountType: this.domainOrCloudAccount,
+          authAccountType: accountType,
         })
       })
       this.staffDataArrayEdit && this.staffDataArrayEdit.forEach(item => {
@@ -307,7 +308,7 @@
           authAccount: item.authAccount,
           authPerm: dlpPermission.AuthPermType.CONTENT_EDIT,
           permExpiryTime: Date.UTC(2025, 1, 1),
-          authAccountType: this.domainOrCloudAccount,
+          authAccountType: accountType,
         })
       })
     }
@@ -407,12 +408,13 @@
           }
           // foreach
           this.dlpFile.dlpProperty.authUsers = []
+          const accountType = this.domainOrCloudAccount;
           this.staffDataArrayReadOnly && this.staffDataArrayReadOnly.forEach(item => {
             this.dlpFile.dlpProperty.authUsers.push({
               authAccount: item.authAccount,
               authPerm: dlpPermission.AuthPermType.READ_ONLY,
               permExpiryTime: Date.UTC(2025, 1, 1),
-              authAccountType: this.domainOrCloudAccount,
+              authAccountType: accountType,
             })
           })
           this.staffDataArrayEdit && this.staffDataArrayEdit.forEach(item => {
@@ -421,7 +423,7 @@
               authAccount: item.authAccount,
               authPerm: dlpPermission.AuthPermType.CONTENT_EDIT,
               permExpiryTime: Date.UTC(2025, 1, 1),
-              authAccountType: this.domainOrCloudAccount,
+              authAccountType: accountType,
             })
           })
         }


```

## [17/50] ID: OH_0381 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/MainAbility/pages/index.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let [key, value] of this.pathLengths.entries()) {
        dashOffsetImage = Math.round(this.mapRangeClamped(this.countDownFromImage, 0, this.ANIM_LINES_DRAW_END, value, 0));
        var nn = key + " { stroke-dasharray: " + value + " " + value + "; stroke-dashoffset: " + dashOffsetImage + "; } "
        this.cssStr = this.cssStr + nn
      }
```

### Patch
```diff
// File: entry/src/main/ets/MainAbility/pages/index.ets
--- a/entry/src/main/ets/MainAbility/pages/index.ets
+++ b/entry/src/main/ets/MainAbility/pages/index.ets
@@ -128,7 +128,9 @@
               .margin({ top: 10 })
               .textAlign(TextAlign.Center)
             Stack() {
-              ForEach(this.cherrys, (item: Cherry) => {
+              // Cache state variable to avoid frequent reads in loop
+              const cherrysCache = this.cherrys;
+              ForEach(cherrysCache, (item: Cherry) => {
                 SVGImageView({
                   svgString: SVGExample.cherrySvg,
                   x: item.x,


```

## [18/50] ID: OH_0132 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/index.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let index:number = startNum; index <= endNum; index++) {
            this.cusRangeArr.push(index);
          }
```

### Patch
```diff
// File: entry/src/main/ets/pages/index.ets
--- a/entry/src/main/ets/pages/index.ets
+++ b/entry/src/main/ets/pages/index.ets
@@ -1317,14 +1317,16 @@
     let size = this.mediaSize.get300PixelMediaSize();
     let fileList = new Array<number>();
     let imageSourceIndexList = new Array<number>();
-    for (let index = 0; index < this.printRange.length; index++) {
-      imageSourceIndexList.push(this.printRange[index] - 1);
+    const printRange = this.printRange;
+    for (let index = 0; index < printRange.length; index++) {
+      imageSourceIndexList.push(printRange[index] - 1);
     }
     Log.info(TAG, 'imageSourceIndexList: ', JSON.stringify(imageSourceIndexList))
     let len = imageSourceIndexList.length;
+    const imageSources = this.imageSources;
     for (let index = 0; index < len; index++) {
-      Log.info(TAG,'imageModel START ,this.imageSources '+JSON.stringify(this.imageSources))
-      let imageModel = this.imageSources[imageSourceIndexList[index]];
+      Log.info(TAG,'imageModel START ,this.imageSources '+JSON.stringify(imageSources))
+      let imageModel = imageSources[imageSourceIndexList[index]];
       Log.info(TAG,'imageModel: '+JSON.stringify(imageModel))
       let offCanvas, scale, offCanvasWidth, offCanvasHeight, orientation
       if (this.pageDirection === PageDirection.VERTICAL || (this.pageDirection === PageDirection.AUTO && imageModel.height >= imageModel.width)) {


```

## [19/50] ID: OH_0267 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `feature/uikit/src/main/ets/component/MenuGroupComponent.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export struct WifiMenuGroupComponent {
  tag: string = 'WifiMenuGroupComponent : ';
  menuSection: MenuSection | undefined;
  style: CardSectionListStyle = cardSectionListStyle;
  controller: MenuController | undefined = undefined;
  @State @Watch('uiRefresherWatch') uiRefresher: UiRefresher = new UiRefresher();
  @State lazyWifiMenus: MenuDataSource = new MenuDataSource([])
  COUNT_EMPTY: number = 0;

  uiRefresherWatch(): void {
    this.getWifiMenus();
  }

  build() {
    Column() {
      Column() {
        if (this.menuSection?.getHeader()) {
          MenuGroupItemComponent({ menuGroup: this.menuSection.getHeader() });
        }
      }

      Column() {
        Column() {
          if (this.lazyWifiMenus.totalCount() > this.COUNT_EMPTY) {
            List() {
              LazyForEach(this.lazyWifiMenus, (menu: SettingsBaseMenu) => {
                ListItem() {
                  WifiEntryComponent({
                    menu: menu as SettingsBaseMenu,
                    style: menu.style as DefaultEntryMenuStyle,
                    showTitle: menu.title?.toString(),
                  });
                }
                .backgroundColor(this.style?.backgroundColor)
              }, (menu: SettingsBaseMenu) => {
                return menu.toString();
              });
            }
            .backgroundColor(this.style?.backgroundColor)
            .cachedCount(DEFAULT_CACHE_COUNT)
            .edgeEffect(EdgeEffect.None)
            .scrollBar(BarState.Off)
            .divider({
              strokeWidth: this.style?.divider?.strokeWidth ?? 0,
              color: this.style?.divider?.color,
              startMargin: this.style?.divider?.startMargin,
              endMargin: this.style?.divider?.endMargin,
            })
            .alignSelf(ItemAlign.Start)
            .clip(true)
            .lanes(this.style?.lanes)
            .borderRadius(this.style?.borderRadius)
            .padding({
              top: $r('app.float.padding_4'),
              bottom: $r('app.float.padding_4'),
            })
            // 只有一个Ap时，可能是“添加其他网络”的占位，所以这种情况，也不展示列表。
            .visibility((this.uiRefresher.isVisible() && this.lazyWifiMenus.totalCount() > this.COUNT_EMPTY &&
              this.lazyWifiMenus.getData(0)?.key) ? Visibility.Visible : Visibility.None);
          }
        }
        .padding({
          bottom: $r('app.float.margin_24')
        })
      }
      .size({ width: '100%' })

      Column() {
        if (this.menuSection?.getFooter()) {
          MenuGroupItemComponent({ menuGroup: this.menuSection?.getFooter() });
        }
      }
    }
    .visibility(this.uiRefresher.isVisible() ? Visibility.Visible : Visibility.None);
  }

  private getWifiMenus(): void {
    let menus = this.menuSection?.getMenus() ?? [];
    LogUtil.info(`${this.tag} get app list, size:  ${menus.length}`);
    this.lazyWifiMenus.refreshData(menus);
  }

  aboutToAppear(): void {
    LogUtil.info(`${this.tag} aboutToAppear ${this.menuSection?.getLogKey()}`);
    this.controller = this.menuSection?.getControllerInstance(this.uiRefresher) as MenuController;
    this.getWifiMenus();
  }

  aboutToDisappear(): void {
    LogUtil.info(`${this.tag} aboutToDisappear ${this.menuSection?.getLogKey()}`);
    this.controller?.aboutToDisappear();
  }
}
```

### Patch
```diff
// File: feature/uikit/src/main/ets/component/MenuGroupComponent.ets
--- a/feature/uikit/src/main/ets/component/MenuGroupComponent.ets
+++ b/feature/uikit/src/main/ets/component/MenuGroupComponent.ets
@@ -458,6 +458,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct MenuGroupItemComponent {
   tag: string = 'MenuGroupItemComponent : ';
@@ -767,6 +768,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct MenuItemComponent {
   tag: string = 'MenuItemComponent : ';
@@ -960,6 +962,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct SettingHomeMenuItemComponent {
   tag: string = 'SettingHomeMenuItemComponent : ';
@@ -1159,6 +1162,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct HotSpotFlatEntryMenuComponent {
   tag: string = 'FlatEntryMenuComponent : ';


```

## [20/50] ID: OH_0166 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let i = 0; i < bundleNames.length; i++) {
      // Get BundleInfo based on bundle name
      bundle.getBundleInfo(bundleNames[i], Constants.PARMETER_BUNDLE_FLAG).then(res => {
        Promise.all([getAppLabel(res.appInfo.labelId, res.name),
        getAppIcon(res.appInfo.iconId, res.name)
        ])
          .then((values) => {
            this.applicationList[i] = (
              new ApplicationObj(
              String(values[0]),
              String(values[1]),
                i,
                res.appInfo.accessTokenId,
                routerData[0].permission,
              makePy(values[0])[0].slice(0, 1)) // Get the first letter in the returned initials array
            );
            this.oldApplicationItem[i] = (
              new ApplicationObj(
              String(values[0]),
              String(values[1]),
                i,
                res.appInfo.accessTokenId,
                routerData[0].permission,
              makePy(values[0])[0].slice(0, 1)) // Get the first letter in the returned initials array
            );
          });
        // 0: have permission; -1: no permission
        var boole = true;
        this.permissionNum++;
        for (let j = 0; j < routerData.length; j++) {
          if (res.reqPermissions.indexOf(routerData[j].permission) == -1) {
            continue
          }
          verifyAccessToken(res.appInfo.accessTokenId, routerData[j].permission).then((access) => {
            if (Number(access) === Constants.PERMISSION_INDEX) {
              if(boole){
                this.toggleIsOn[i] = true;
              }
            } else {
              if(boole){
                this.permissionNum--
              }
              boole = false;
              this.toggleIsOn[i] = false;
            }
          });
        }
      }).catch(error => {
        console.log(TAG + bundleNames[i] + "getBundleInfo failed, cause: " + JSON.stringify(error));
      })
    }
```

### Patch
```diff
// File: permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
--- a/permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
+++ b/permissionmanager/src/main/ets/pages/authority-tertiary-groups.ets
@@ -167,8 +167,9 @@
                         _this.toggleIsOn[item.index] = true;
                       }
                       let num = Constants.PERMISSION_NUM;
-                      for(let key in _this.toggleIsOn){
-                        if(_this.toggleIsOn[key]){
+                      const toggleState = _this.toggleIsOn;
+                      for(let key in toggleState){
+                        if(toggleState[key]){
                           num++;
                         }
                       }
@@ -189,8 +190,9 @@
                         _this.toggleIsOn[item.index] = false;
                       }
                       let num = Constants.PERMISSION_NUM;
-                      for(let key in _this.toggleIsOn){
-                        if(_this.toggleIsOn[key]){
+                      const toggleState = _this.toggleIsOn;
+                      for(let key in toggleState){
+                        if(toggleState[key]){
                           num++;
                         }
                       }


```

## [21/50] ID: OH_0281 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `product/phone/src/main/ets/Setting/Wlan/WifiWindowSettings.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct WifiWindowSettings {
  private dataSource: ControlCenterWlanDataSource = new ControlCenterWlanDataSource();
  private session: UIExtensionContentSession | undefined =
    storage?.get<UIExtensionContentSession>('wifiExtensionSession');
  private wifiControlCenterPageController: WifiControlCenterPageController = new WifiControlCenterPageController();
  // 当前是否在外屏
  private isOuterScreen: boolean = CommonUtils.isOuterScreen();
  @StorageLink('WlanListLoadingVisible') loadingVisible: boolean = false;
  @State controlCenterColor: ResourceColor = $r('app.color.control_center_sub_panel_color');
  @State isHover: boolean = false;

  build() {
    Column() {
      this.wifiWindowTitleBuilder()

      this.wifiListBuilder()

      if (!this.isOuterScreen) {
        this.moreWifiSettingBuilder()
      }
    }
    .padding({
      top: $r('app.float.wh_value_16'),
      bottom: $r('app.float.wh_value_16'),
    })
    .size({ width: '100%', height: '100%' })
    .borderRadius($r('app.float.wh_value_32'))
    .onAppear(() => {
      AccessibilityUtils.requestFocusAccessibilityWithBundleName(WINDOW_WLAN_TITLE);
    })
  }

  @Builder
  wifiWindowImageBuilder() {
    Image($r('app.media.ic_wifi_signal_4'))
      .fillColor($r('app.color.window_settings_icon_primary'))
      .advancedBlendMode(BlendModeUtil.getCenterBlender())
      .draggable(false)
      .size({
        width: $r('app.float.wh_value_24'),
        height: $r('app.float.wh_value_24')
      })
      .margin({
        bottom: $r('app.float.wh_value_8'),
        end: this.isOuterScreen ? PADDING_8 : undefined,
      })
  }

  @Builder
  wifiWindowWlanTextBuilder() {
    Text($r('app.string.wifi_settings_title'))
      .fontFamily('HarmonyHeiTi')
      .fontWeight(FontWeight.Medium)
      .advancedBlendMode(BlendModeUtil.getCenterBlender())
      .fontSize($r('sys.float.ohos_id_text_size_headline8'))
      .fontColor($r('app.color.window_settings_font_primary'))
      .lineHeight($r('app.float.wh_value_26'))
      .height($r('app.float.wh_value_26'))
      .id(WINDOW_WLAN_TITLE)
  }

  @Builder
  wifiWindowTitleBuilder() {
    if (this.isOuterScreen) {
      Row() {
        this.wifiWindowImageBuilder()
        this.wifiWindowWlanTextBuilder()
        LoadingProgress()
          .width($r('app.float.width_24'))
          .height($r('app.float.height_24'))
          .margin({
            start: PADDING_44
          })
          .id('loading_progress_wifi_list_group')
          .visibility(this.loadingVisible ? Visibility.Visible : Visibility.Hidden)
          .position({
            end: PADDING_36
          })
      }
      .width('100%')
      .padding({
        bottom: $r('app.float.wh_value_24'),
      })
      .justifyContent(FlexAlign.Center)
    } else {
      Column() {
        this.wifiWindowImageBuilder()
        this.wifiWindowWlanTextBuilder()
      }
      .width('100%')
      .padding({
        bottom: $r('app.float.wh_value_24'),
      })
      .alignItems(HorizontalAlign.Center)
    }
  }

  @Builder
  moreWifiSettingBuilder() {
    Column() {
      Text($r('app.string.wifi_more_settings'))
        .fontFamily('HarmonyHeiTi')
        .fontWeight(FontWeight.Medium)
        .fontSize($r('app.float.font_16'))
        .fontColor(this.controlCenterColor)
        .lineHeight($r('app.float.font_21'))
        .width('100%')
        .textAlign(TextAlign.Center)
        .maxFontScale(2)
    }
    .onClick(() => {
      HiSysEventUtil.reportDefaultBehaviorEventByUE(HiSysAboutBluetoothEventGroup.ENTER_SETTINGS_WIFI_PAGE);
      this.onMoreSettingClick();
    })
    .alignItems(HorizontalAlign.Center)
    .margin({
      top: $r('app.float.wh_value_15'),
      left: $r('app.float.wh_value_16'),
      right: $r('app.float.wh_value_16'),
    })
    .padding({
      top: $r('app.float.wh_value_9'),
      bottom: $r('app.float.wh_value_10'),
    })
    .stateStyles({
      normal: this.normalStyles,
      pressed: this.buttonPressedStyles,
    })
    .onHover((isHover?: boolean) => {
      this.isHover = isHover ?? false;
    })
  }

  @Builder
  wifiListBuilder() {
    Column() {
      List() {
        this.wifiListContentBuilder()
      }
      .padding({
        left: $r('app.float.wh_value_8'),
        right: $r('app.float.wh_value_8'),
      })
      .width('100%')
      .height('100%')
      .cachedCount(DEFAULT_CACHE_COUNT)
      .divider({
        strokeWidth: px2vp(1),
        color: $r('app.color.wlan_window_settings_divider_color'),
        startMargin: $r('app.float.wh_value_56'),
        endMargin: $r('app.float.wh_value_20'),
      })
      .alignSelf(ItemAlign.Start)
      .clip(true)
      .edgeEffect(EdgeEffect.Spring, {alwaysEnabled: true})
    }
    .layoutWeight(1)
  }

  @Builder
  wifiListContentBuilder() {
    LazyForEach(this.dataSource, (item: ApMenu) => {
      ListItem() {
        WifiWindowItemComponent({
          menu: item,
          controlCenterColor: this.controlCenterColor,
        })
      }
    }, (item: ApMenu) => {
      let stateIconId: string = (item.stateIcon as Resource)?.id?.toString() || '';
      return `${item?.toString()}${stateIconId}${item.index}`;
    })
  }

  @Styles
  normalStyles() {
    .backgroundColor(this.isHover ? $r('sys.color.interactive_hover') : Color.Transparent)
    .borderRadius($r('app.float.wh_value_20'))
  }

  @Styles
  buttonPressedStyles() {
    .backgroundColor(this.isHover ? $r('sys.color.interactive_hover') : $r('sys.color.interactive_click'))
    .borderRadius($r('app.float.wh_value_20'))
  }

  onMoreSettingClick(): void {
    let bundleName: string = PackagesConstant.SETTINGS_BUNDLE_NAME;
    let abilityName: string = PackagesConstant.SETTINGS_MAIN_ABILITY_NAME;
    let navEntryKey: string = NavEntryKey.WIFI_ENTRY;
    let message: string = `bundleName: ${bundleName}, abilityName: ${abilityName}, navEntryKey: ${navEntryKey}`;
    HiSysEventUtil.reportEntryEvent(ENTER_EXTERNAL_ENTRY, message);
    LogUtil.info(`${TAG} onMoreSettingClick startAbilityForResult ${message}`);
    AbilityUtils.startAbilityForResult({
      bundleName: bundleName,
      abilityName: abilityName,
      uri: navEntryKey,
      parameters: {
        // 从更多设置进入wifi详情页
        fromMoreSetting: true
      }
    }, () => {
      this.session?.sendData({ 'method': 'hideControlCenter' });
    });
  }

  aboutToAppear(): void {
    LogUtil.info(`${TAG} aboutToAppear `);
    this.initSessionReceiveDataCallback();
    this.wifiControlCenterPageController.bindList(this.dataSource);
    this.wifiControlCenterPageController.aboutToAppear();
  }

  aboutToDisappear(): void {
    LogUtil.info(`${TAG} aboutToDisappear`);
    this.wifiControlCenterPageController.aboutToDisappear();
  }

  /**
   * 监听拉起方发送的数据
   */
  private initSessionReceiveDataCallback(): void {
    try {
      this.session?.setReceiveDataCallback((data: ReceiveData) => {
        const controlCenterSubPanelColor = data?.controlCenterColor;
        if (typeof controlCenterSubPanelColor === 'number') {
          LogUtil.info(`${TAG} setReceiveDataCallback new controlCenterColor:${controlCenterSubPanelColor}`);
          this.controlCenterColor = controlCenterSubPanelColor;
        }
      })
    } catch (error) {
      LogUtil.error(`${TAG} setReceiveDataCallback catch error. code:${error?.code} message:${error?.message}`);
    }
  }

  onPageShow(): void {
    LogUtil.info(`${TAG} onPageShow`);
    this.wifiControlCenterPageController.onPageShow();
    WifiUtils.publishEnterWlanPageEvent(true);
    HiSysEventUtil.reportDefaultBehaviorEventByUE(HiSysAboutBluetoothEventGroup.CLICK_WLAN_TEXT_SHOW_DIALOG);
  }

  onPageHide(): void {
    LogUtil.info(`${TAG} onPageHide, send hideSubPage message.`);
    this.wifiControlCenterPageController.onPageHide();
    // 某些特殊场景下，关闭wifi控制中心窗口的时候无触碰事件，这会导致后续点击其他控制中心按钮无法弹窗，发hideSubPage消息可以解决
    this.session?.sendData({ 'method': 'hideSubPage' });
    WifiUtils.publishEnterWlanPageEvent(false);
  }
}
```

### Patch
```diff
// File: product/phone/src/main/ets/Setting/Wlan/view/controlCenter/WifiWindowItemComponent.ets
--- a/product/phone/src/main/ets/Setting/Wlan/view/controlCenter/WifiWindowItemComponent.ets
+++ b/product/phone/src/main/ets/Setting/Wlan/view/controlCenter/WifiWindowItemComponent.ets
@@ -24,6 +24,7 @@
 /**
  * 控制中心wlan列表item组件
  */
+@Reusable
 @Component
 export struct WifiWindowItemComponent {
   private controlCenterColor: ResourceColor = $r('app.color.control_center_sub_panel_color');


```

## [22/50] ID: OH_0181 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-local-var-to-replace-state-var`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/pages/dialogPlus.ets`
- **Warning:** Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
if (this.reqPerms == undefined || this.accessTokenId == undefined || this.reqPerms.length == 0) {
      Log.info('invalid parameters');
      this.initStatus = Constants.INIT_NEED_TO_TERMINATED;
      return;
    }
```

### Patch
```diff
// File: permissionmanager/src/main/ets/pages/dialogPlus.ets
--- a/permissionmanager/src/main/ets/pages/dialogPlus.ets
+++ b/permissionmanager/src/main/ets/pages/dialogPlus.ets
@@ -71,7 +71,6 @@
   @State appName: string = '';
   @State locationFlag: number = Constants.LOCATION_NONE;
   @State reqPermissionDetails: bundleManager.ReqPermissionDetail[] = [];
-  @State refresh: number = 0;
   @State pasteBoardName: string = '';
   @State isUpdate: number = -1;
 
@@ -155,7 +154,7 @@
                         })
                         Span(this.currentGroup().reason ? $r('app.string.comma') : $r('app.string.period'))
                       }
-                      Span(this.refresh >= 0 ? this.currentGroup().reason : '')
+                      Span(this.currentGroup().reason)
                     }
                   }
                   .textAlign(TextAlign.Start)
@@ -539,7 +538,6 @@
             context.resourceManager.getStringValue(reqPermissionDetail.reasonId, (err, value) => {
               if (value !== undefined && group.reason === '') {
                 group.reason = value.slice(Constants.START_SUBSCRIPT, Constants.END_SUBSCRIPT);
-                this.refresh ++;
               }
               this.initStatus = Constants.INIT_NEED_TO_REFRESH;
             })


```

## [23/50] ID: OH_0005 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `entry/src/main/ets/MainAbility/pages/dialer/callRecord/AllRecord.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct RecordView {
  @Link private mPresenter: any

  build() {
    Stack() {
      List() {
        LazyForEach(this.mPresenter.mAllCallRecordListDataSource, (item, index: number) => {
          ListItem() {
            ContactItem({ mPresenter: $mPresenter, item: item });
          }
          .height($r("app.float.id_item_height_max"))
        }, item => item.id)
      }
      .divider({
        strokeWidth: 1,
        color: $r('sys.color.ohos_id_color_list_separator'),
        startMargin: $r("app.float.id_item_height_sm"),
        endMargin: $r("app.float.id_card_margin_max"),
      })
      .margin({ bottom: '110vp' })
    }
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/MainAbility/pages/dialer/callRecord/AllRecord.ets
--- a/entry/src/main/ets/MainAbility/pages/dialer/callRecord/AllRecord.ets
+++ b/entry/src/main/ets/MainAbility/pages/dialer/callRecord/AllRecord.ets
@@ -83,6 +83,7 @@
 }
 
 
+@Reusable
 @Component
 struct ContactItem {
   @Link mPresenter: CallRecordPresenter


```

## [24/50] ID: OH_0101 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 2`
- **Target File:** `entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSelectMemSendMsg.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct IntelligenceGroupContactsList {
  @Link presenter: IntelligenceGroupSelectMemSendMsgPresenter;
  // Scrolling Parameters
  private scroller: Scroller = new Scroller();
  @State alphabetSelected: number = 0;
  @State isAlphabetClicked: boolean = false;
  @State dragList: boolean = false;
  @State alphabetIndexPresenter: AlphabetIndexerPresenter = this.presenter.alphabetIndexPresenter;
  @State isPC: boolean = EnvironmentProp.isPC();
  @StorageLink('isShowSmartWindow') isShowSmartWindow: boolean = false;
  @StorageProp('fontSizeScale') fontSizeScale: number = 0;
  @StorageProp('splitStatus') splitStatus: SplitStatus = SplitStatus.DEFAULT;
  @StorageLink('sceillOnlenth') sceillOnlenth: number = 0;
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;
  @StorageLink('breakpoint') curBp: string = 'sm';

  build() {
    Column() {
      Stack({ alignContent: Alignment.TopEnd }) {
        List({ initialIndex: this.presenter.initialIndex, scroller: this.scroller }) {
            LazyForEach(this.presenter.contactsSource, (item: BatchSelectContact) => {
              ListItem() {
                SelectContactItemView({
                  item: item.contact,
                  index: item.index,
                  onContactItemClicked: (index, indexChild): void =>
                  this.presenter.onContactItemClicked(index, indexChild),
                  showIndex: item.showIndex,
                  showDivifer: item.showDivifer
                })
              }
              .width('100%')
            }, (item: BatchSelectContact) => JSON.stringify(item))
        }

        .width('100%')
        .padding({ right: this.isShowSmartWindow ? $r('app.float.id_card_margin_xxl_minus') : 0 })
        .height('100%')
        .listDirection(Axis.Vertical)
        .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
        .scrollBar(BarState.Off)
        .onScrollIndex((firstIndex: number, lastIndex: number) => {
          this.presenter.sceillOnlenth = ( lastIndex - firstIndex) + 1
          this.presenter.resetInitialIndex(firstIndex);
          if (!this.isAlphabetClicked && this.dragList) {
            this.alphabetSelected = this.alphabetIndexPresenter.getAlphabetSelected(firstIndex);
          }
        })
        .onScrollStart(() => {
          emitter.emit(AlphabetIndexerPage.innerEvent);
          this.dragList = true;
          this.isAlphabetClicked = false;
        })
        .onScrollStop(() => {
          this.isAlphabetClicked = true;
          this.dragList = false;
        })
        .clipContent(ContentClipMode.SAFE_AREA)
        .safeAreaPadding({ top: this.isPC ? 0 : '94' })

        if (DisplaySplitUtil.isShowIndex(this.splitStatus)) {
          IntelligenceGroupAlphabetIndexerPage({
            scroller: this.scroller,
            presenter: $alphabetIndexPresenter,
            selected: this.alphabetSelected,
            isClicked: $isAlphabetClicked,
            isAutoCollapse: true,
            scrollIndexOffset: false
          })
            .margin({
              top: this.isPC ? '16vp' : '110vp',
              bottom: '10%',
              right: this.isPC ? '4vp' : '0vp',
              left: '4vp'
            })
            .visibility((this.presenter.inputKeyword !== '' || this.isShowSmartWindow)
              ? Visibility.None : Visibility.Visible)
        }
      }
    }
    .width('100%')
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSelectMemSendMsg.ets
--- a/entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSelectMemSendMsg.ets
+++ b/entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSelectMemSendMsg.ets
@@ -490,6 +490,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct SelectContactItemView {
   @State private single: boolean = false;


```

## [25/50] ID: OH_0355 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/view/WaterFlowNodeView.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export struct WaterFlowNodeView {
  @StorageLink(BreakpointConstants.BREAKPOINT_NAME) currentBreakpoint: string = BreakpointConstants.BREAKPOINT_SM;
  index: number = 0;
  dataSource: WaterFlowDataSource = new WaterFlowDataSource();
  // 节点工厂实例
  private typeCfg: TypeReuseConfig = {
    type: REUSE_VIEW_TYPE_ITEM,
    expirationTime: 30 * 60 * 1000, // 老化时间
    reuseCallback: this.reuseCallback,
    recycleCallback: this.recycleCallback
  }

  private reuseCallback(item: NodeItem): void {
    if (item?.data?.item instanceof ViewItem) {
      let newItem: ViewItem = item.data.item as ViewItem;
      newItem.shouldClearImageCache = false;
    }
  }

  private recycleCallback(item: NodeItem): void {
    if (item?.data?.item instanceof ViewItem) {
      let newItem: ViewItem = item.data.item as ViewItem;
      newItem.shouldClearImageCache = true;
    }
  }

  aboutToAppear(): void {
    nodePoolItem.setTypeReuseConfig(this.typeCfg);
    // 添加模拟数据
    switch (this.index) {
      case 0:
        this.dataSource.addItems(recommendData());
        break;
      case 1:
        this.dataSource.addItems(surroundData());
        break;
      case 2:
        this.dataSource.addItems(outTravelData());
        break;
      case 3:
        this.dataSource.addItems(selfDriveData());
        break;
      case 4:
        this.dataSource.addItems(mountainData());
        break;
      case 5:
        this.dataSource.addItems(parentingData());
        break;
      case 6:
        this.dataSource.addItems(freeWalkerData());
        break;
      case 7:
        this.dataSource.addItems(campingData());
        break;
    }
  }

  build() {
    Column({ space: CommonConstants.SPACE_EIGHT }) {
      Column() {
        WaterFlow() {
          LazyForEach(this.dataSource, (item: ViewItem, index: number) => {
            FlowItem() {
              NodeContainerProxy({
                nodeItem: nodePoolItem.getNode(REUSE_VIEW_TYPE_ITEM, {
                  item: item
                }, flowItemWrapper)
              })
            }
            .width($r('app.string.nodepool_percent_100'))
            .backgroundColor(Color.White)
            .clip(true)
            .borderRadius($r('app.float.common_border_radius_7'))
          }, (index: string) => index)
        }
        .cachedCount(3)
        .nestedScroll({ scrollForward: NestedScrollMode.PARENT_FIRST, scrollBackward: NestedScrollMode.SELF_FIRST })
        .columnsTemplate(new BreakpointType({
          sm: BreakpointConstants.GRID_NUM_TWO,
          md: BreakpointConstants.GRID_NUM_THREE,
          lg: BreakpointConstants.GRID_NUM_FOUR
        }).getValue(this.currentBreakpoint))
        .columnsGap($r('app.float.waterflow_columns_gap'))
        .rowsGap($r('app.float.waterflow_rows_gap'))
        .layoutDirection(FlexDirection.Column)
        .itemConstraintSize({
          minWidth: CommonConstants.ZERO_PERCENT,
          maxWidth: CommonConstants.FULL_PERCENT,
          minHeight: CommonConstants.ZERO_PERCENT,
        });
      }
      .width(CommonConstants.FULL_PERCENT)
      .height(CommonConstants.FULL_PERCENT)
    }
    .height(CommonConstants.FULL_PERCENT)
    .margin({
      top: $r('app.float.margin_8'),
      left: new BreakpointType({
        sm: BreakpointConstants.SEARCHBAR_AND_WATER_FLOW_MARGIN_LEFT_SM,
        md: BreakpointConstants.SEARCHBAR_AND_WATER_FLOW_MARGIN_LEFT_MD,
        lg: BreakpointConstants.SEARCHBAR_AND_WATER_FLOW_MARGIN_LEFT_LG
      }).getValue(this.currentBreakpoint),
      right: new BreakpointType({
        sm: BreakpointConstants.SEARCHBAR_AND_WATER_FLOW_MARGIN_RIGHT_SM,
        md: BreakpointConstants.SEARCHBAR_AND_WATER_FLOW_MARGIN_RIGHT_MD,
        lg: BreakpointConstants.SEARCHBAR_AND_WATER_FLOW_MARGIN_RIGHT_LG
      }).getValue(this.currentBreakpoint)
    })
    .animation({
      duration: CommonConstants.ANIMATION_DURATION_TIME,
      curve: Curve.EaseOut,
      playMode: PlayMode.Normal
    });
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/view/WaterFlowNodeView.ets
--- a/entry/src/main/ets/view/WaterFlowNodeView.ets
+++ b/entry/src/main/ets/view/WaterFlowNodeView.ets
@@ -47,6 +47,7 @@
 export let nodePoolItem = nodePoolFactory.getCommonNodePool();
 
 // 自定义组件复用池Swiper页面
+@Reusable
 @Component
 export struct WaterFlowNodeView {
   @StorageLink(BreakpointConstants.BREAKPOINT_NAME) currentBreakpoint: string = BreakpointConstants.BREAKPOINT_SM;


```

## [26/50] ID: OH_0207 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 2`
- **Target File:** `SliderPlayer/src/main/ets/components/SwipePlayer.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export struct SwipePlayer {
  @State curIndex: number = 0;
  @Require swipePlayerController!: SwipePlayerController;
  private readonly tag: string = 'SwipePlayer --'
  private datasource: SwipePlayerIDataSource = new SwipePlayerIDataSource();
  private swiperController: SwiperController = new SwiperController();
  private avPlayerMgr: AVPlayerMgr = new AVPlayerMgr();
  private options?: SwipePlayerOptions;
  private windowMgr: WindowMgr = WindowMgr.getInstance();
  private swiperCachedCount: number = 1;

  aboutToAppear(): void {
    this.setCacheCount();
    this.swipePlayerController?.set(this.avPlayerMgr);
    WindowMgr.getInstance().setUIContext(this.getUIContext())
    window.getLastWindow(this.getUIContext().getHostContext(), (err: BusinessError, data) => {
      if (err.code) {
        Logger.error('%{public}s Failed to obtain the top window. Code: %{public}d, message: %{public}s', this.tag,
          err.code, err.message);
      }
      this.windowMgr.setWindowStage(data);
    });
  }

  setCacheCount() {
    if (this.options?.cachedCount) {
      if (this.options.cachedCount > 3) {
        this.swiperCachedCount = 3;
      } else if (this.options.cachedCount < 0) {
        this.swiperCachedCount = 0;
      } else {
        this.swiperCachedCount = this.options.cachedCount;
      }
    } else if (this.options?.cachedCount === 0) {
      this.swiperCachedCount = 0;
    } else {
      this.swiperCachedCount = 1;
    }

  }

  build() {
    Column() {
      Stack({ alignContent: Alignment.TopStart }) {
        Swiper(this.swiperController) {
          LazyForEach(this.datasource,
            (item: VideoSwipePlayerDataSource | CustomSwipePlayerDataSource, index: number) => {
              VideoSwipeComponent({
                index: index,
                datasource: item,
                curIndex: this.curIndex,
                avPlayerMgr: this.avPlayerMgr,
                swipePlayerController: this.swipePlayerController
              });
            },
            (item: VideoSwipePlayerDataSource | CustomSwipePlayerDataSource, index: number) => JSON.stringify(item) +
              index);
        }
        .cachedCount(this.swiperCachedCount)
        .width(CommonConstant.FULL_PERCENT_WIDTH)
        .height(CommonConstant.FULL_PERCENT_HEIGHT)
        .vertical(true)
        .loop(false)
        .curve(Curve.Ease)
        .duration(CommonConstant.DURATION_TIME)
        .indicator(false)
        .backgroundColor(Color.Black)
        .effectMode(this.curIndex === 0 ? EdgeEffect.None : EdgeEffect.Spring)
        .onChange((index: number) => {
          if (this.options?.swiperCallback?.onChange) {
            this.options.swiperCallback?.onChange(index);
          }
        })
        .onAnimationStart((index: number, targetIndex: number, extraInfo: SwiperAnimationEvent) => {
          this.curIndex = targetIndex;
          if (this.options?.swiperCallback?.onAnimationStart) {
            this.options.swiperCallback?.onAnimationStart(index, targetIndex, extraInfo);
          }
        })
        .onAnimationEnd((index: number, extraInfo: SwiperAnimationEvent) => {
          if (this.options?.swiperCallback?.onAnimationEnd) {
            this.options.swiperCallback?.onAnimationEnd(index, extraInfo);
          }
        })
      }
    }
    .width(CommonConstant.FULL_PERCENT_WIDTH)
    .height(CommonConstant.FULL_PERCENT_HEIGHT)
  }
}
```

### Patch
```diff
// File: SliderPlayer/src/main/ets/components/VideoSwipeComponent.ets
--- a/SliderPlayer/src/main/ets/components/VideoSwipeComponent.ets
+++ b/SliderPlayer/src/main/ets/components/VideoSwipeComponent.ets
@@ -19,6 +19,7 @@
 import { VideoSwipeCustom } from './VideoSwipeCustom';
 import { VideoSwipePlayer } from './VideoSwipePlayer';
 
+@Reusable
 @Component
 export struct VideoSwipeComponent {
   @Prop index: number;


```

## [27/50] ID: OH_0364 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `feature/pagedesktop/src/main/ets/default/common/components/SwiperPage.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let i = 0; i < row; i++) {
      this.rowsTemplate += '1fr '
    }
```

### Patch
```diff
// File: feature/pagedesktop/src/main/ets/default/common/components/SwiperPage.ets
--- a/feature/pagedesktop/src/main/ets/default/common/components/SwiperPage.ets
+++ b/feature/pagedesktop/src/main/ets/default/common/components/SwiperPage.ets
@@ -187,6 +187,9 @@
   }
 
   build() {
+    const cachedPaddingTop = this.mPaddingTop;
+    const cachedNameLines = this.mNameLines;
+    const cachedFormRefresh = this.formRefresh;
     Grid() {
       ForEach(this.mAppListInfo, (item: LauncherDragItemInfo, index: number) => {
         GridItem() {
@@ -196,13 +199,13 @@
             AppItem({
               item: item,
               mPageDesktopViewModel: this.mPageDesktopViewModel,
-              mNameLines: this.mNameLines
+              mNameLines: cachedNameLines
             }).id(`${TAG}_AppItem_${index}`)
           } else if (item.typeId === CommonConstants.TYPE_FOLDER) {
             FolderItem({
               folderItem: item,
               mPageDesktopViewModel: this.mPageDesktopViewModel,
-              mNameLines: this.mNameLines
+              mNameLines: cachedNameLines
             }).id(`${TAG}_FolderItem_${index}`)
           } else if (item.typeId === CommonConstants.TYPE_CARD) {
             FormItem({
@@ -211,7 +214,7 @@
           }
         }
         .id(`${TAG}_GridItem_${index}`)
-        .padding({ top: this.mPaddingTop })
+        .padding({ top: cachedPaddingTop })
         .rowStart(item.row)
         .columnStart(item.column)
         .rowEnd(this.getRowEnd(item))
@@ -221,7 +224,7 @@
         if (item.typeId === CommonConstants.TYPE_FOLDER) {
           return JSON.stringify(item);
         } else if (item.typeId === CommonConstants.TYPE_CARD) {
-          return JSON.stringify(item) + this.formRefresh;
+          return JSON.stringify(item) + cachedFormRefresh;
         } else if (item.typeId === CommonConstants.TYPE_APP) {
           return JSON.stringify(item);
         } else {


```

## [28/50] ID: OH_0046 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `entry/src/main/ets/pages/favorites/favoriteList.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct FavoriteContent {
  @Link presenter: FavoriteListPresenter;
  @State mPresenter: FavoriteListPresenter = this.presenter;
  isUsuallyShow: boolean = false;

  build() {
     Column() {
      GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
        GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 1, lg: 2 } }) {
          TitleGuide({ mPresenter: $mPresenter });
        }
        GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 2, lg: 4 } }) {
          Column() {
            Text($r('app.string.favorite'))
              .fontSize(30)
              .fontWeight(FontWeight.Bold)
              .fontColor($r('sys.color.ohos_id_color_text_primary'))
              .margin({ bottom: $r('app.float.id_card_margin_sm') })
              .lineHeight(42)
              .margin({ top: 8, bottom: 2 })
          }
          .alignItems(HorizontalAlign.Start)
          .width('100%')
          .height(82)
        }
      }
      GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
        GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 1, lg: 2 } }) {
          List({ space: 0, initialIndex: 0 }) {
            LazyForEach(this.presenter.favoriteDataSource, (item: FavoriteListBean, index: number) => {
              ListItem() {
                FavoriteListItem({ presenter: $mPresenter, item: item, mPresenter: $presenter });
              }
            }, (item: FavoriteListBean) => JSON.stringify(item))
          }
          .scrollBar(BarState.Off)
          .editMode(true)
          .width('100%')
          .height('100%')
          .listDirection(Axis.Vertical)
          .edgeEffect(EdgeEffect.Spring)
        }
      }
      .height('100%')
      .flexShrink(1)
    }
    .padding({ left: 24, right: 24 })
    .height('100%')
    .width('100%')
    .backgroundColor(Color.White)
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/favorites/favoriteList.ets
--- a/entry/src/main/ets/pages/favorites/favoriteList.ets
+++ b/entry/src/main/ets/pages/favorites/favoriteList.ets
@@ -128,6 +128,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct FavoriteListItem {
   @Link presenter: FavoriteListPresenter;


```

## [29/50] ID: OH_0072 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-func-as-arg-for-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets`
- **Warning:** Do not use functions as input parameters for creating reusable components

### Buggy Snippet
```typescript
@Component
export default struct DetailInfoRemarks {
  @Link mPresenter: DetailPresenter;
  @Link selectSimBuilder: SelectDialogBuilder;
  @Link maximum: number;
  @Prop telephoneTotal: number;
  @Prop meettingTotal: number;
  @Prop otherTotal: number;
  @Link moreOptionsFlag: boolean;
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;

  isEmptyDetailInfoRemarks(): boolean {
    return (
      !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.emails) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.aims) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.houses) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.websites) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.relationships) ||
        !ArrayUtil.isEmpty<BaseContackSubInfoModel>(this.mPresenter.contactForm.events)
    )
  }

  // 处理展开更多与未展开更多情况下分割线的显示
  isDividerShow(totalCount: number, index: number): Visibility {
    if (this.moreOptionsFlag) {
      if (totalCount - 1 !== index) {
        return Visibility.Visible
      } else {
        return Visibility.None
      }
    } else {
      if (this.telephoneTotal + this.meettingTotal + index + 1 < this.maximum && totalCount - 1 === index) {
        return Visibility.None
      } else if (this.telephoneTotal + this.meettingTotal + index + 1 < this.maximum && totalCount - 1 !== index) {
        return Visibility.Visible
      } else {
        return Visibility.None
      }
    }
  }

  isItemShow(index: number): Visibility {
    let isVisibility: Visibility = Visibility.None;
    if (this.moreOptionsFlag) {
      isVisibility = Visibility.Visible
    } else {
      if (this.telephoneTotal + this.meettingTotal + index < this.maximum) {
        isVisibility = Visibility.Visible
      } else {
        isVisibility = Visibility.None
      }
    }
    return isVisibility
  }

  build() {
    Column() {
      List() {
        if (this.isEmptyDetailInfoRemarks()) {
          LazyForEach(this.mPresenter.detailInfoRemarksSources, (item: ContactStrInterface, index: number) => {
            if (JSON.parse(item.data).data) {
              ListItem() {
                Column() {
                  DetailInfoListItem({
                    listItem: JSON.parse(item.data),
                    mPresenter: $mPresenter,
                    hasArrow: false,
                  });
                  Divider()
                    .color($r('app.color.skin_ohos_id_color_list_separator'))
                    .strokeWidth('1px')
                    .width('100%')
                    .visibility(this.isDividerShow(this.mPresenter.detailInfoRemarksSources.totalCount(), index))
                    .padding({ left: $r('sys.float.padding_level4'), right: $r('sys.float.padding_level4'), })
                }
              }
              .visibility(this.isItemShow(index))
            }
          }, (item: ContactStrInterface, index: number) => JSON.stringify(item) + JSON.stringify(index))
        }
      }
      .scrollBar(BarState.Off)
      .edgeEffect(EdgeEffect.None)
    }
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets
--- a/entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets
+++ b/entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets
@@ -276,12 +276,12 @@
       maskColor: Color.Transparent,
     })
     // 除了生日项，其它类型 不响应点击事件，否则无障碍语音播报会有问题
-    .onClick(this.listItem.dataType == DataItemType.EVENT ? () => {
-      HiLog.i(TAG, 'DetailInfoListItem onClick');
+    .onClick(() => {
       if (this.listItem.dataType == DataItemType.EVENT) {
+        HiLog.i(TAG, 'DetailInfoListItem onClick');
         this.inShowCalendar = true;
       }
-    } : null)
+    })
     .alignItems(HorizontalAlign.Start)
     .justifyContent(FlexAlign.Center)
     .width('100%')


```

## [30/50] ID: OH_0294 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/component/myphone/FilesList.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

### Buggy Snippet
```typescript
@Component
export struct FilesList {
  @Link fileListSource: FileDataSource

  /**
   * 面包屑
   */
  @Link direList: BreadData[]
  @Link isMulti: boolean
  /**
   * 已选择项数
   */
  @Link checkedNum: number
  /**
   * 列表展示
   */
  @Consume isList: boolean

  build() {
    Column() {
      if (this.fileListSource.dataCount) {
        if (this.isList) {
          this.buildListView()
        } else {
          this.buildGridView()
        }
      } else {
        NoContent()
      }
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  buildListView() {
    List() {
      LazyForEach(this.fileListSource, (item, index) => {
        ListItem() {
          FileListItem({
            fileItem: item,
            fileListSource: $fileListSource,
            direList: $direList,
            checkedNum: $checkedNum,
            isMulti: $isMulti
          })
        }
      }, item => item?.id.toString())
    }
    .align(Alignment.TopStart)
    .edgeEffect(EdgeEffect.None)
  }

  @Builder
  buildGridView() {
    Grid() {
      LazyForEach(this.fileListSource, (item, index) => {
        GridItem() {
          FileListItem({
            fileItem: item,
            fileListSource: $fileListSource,
            direList: $direList,
            checkedNum: $checkedNum,
            isMulti: $isMulti
          })
        }
      }, item => item?.id.toString())
    }
    .columnsTemplate('1fr 1fr 1fr')
    .columnsGap($r('app.float.file_list_columns_gap'))
    .rowsGap($r('app.float.file_list_rows_gap'))
    .padding({ left: $r('app.float.common_padding12'), right: $r('app.float.common_padding12') })
    .height('100%')
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/component/myphone/FilesList.ets
--- a/entry/src/main/ets/pages/component/myphone/FilesList.ets
+++ b/entry/src/main/ets/pages/component/myphone/FilesList.ets
@@ -103,7 +103,7 @@
             isMulti: $isMulti
           })
         }
-      }, item => item?.id.toString())
+      }, item => item?.id.toString(), { cachedCount: 5 })
     }
     .columnsTemplate('1fr 1fr 1fr')
     .columnsGap($r('app.float.file_list_columns_gap'))


```

## [31/50] ID: OH_0243 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/transmitmsg/transmitSearchMsgPage.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export struct ContentListView {
  @Link searchCtrl: TransmitSearchMsgController;
  @StorageLink('hasInfoMsg') hasInfoMsg: boolean = false;
  @StorageLink('unreadTotalOfInfo') unreadTotalOfInfo: number = 0;
  @StorageProp('fontSizeScale') fontSizeScale: number = 1;
  /* 设备是否为pad */
  @State isPad: boolean = false
  // 设备是否为PC
  @State isPC: boolean = DeviceUtil.isPC();
  @StorageLink('mmsPadMargin') padMargin: number = DeviceUtil.padMargin();
  @State isMultiSelectStatus: boolean = false;
  @State isInSetReadThreadIndex: number = -1;

  aboutToAppear(): void {
    this.isPad = DeviceUtil.isTablet();
  }

  build() {
    Column() {
      List() {
        if (this.hasInfoMsg) {
          ListItem() {
            Row() {
              if (this.searchCtrl.isShowHead) {
                SymbolGlyph($r('sys.symbol.bell_fill'))
                  .alignRules({
                    center: { anchor: '__container__', align: VerticalAlign.Center },
                    left: { anchor: '__container__', align: HorizontalAlign.Start }
                  })
                  .renderGroup(true)
                  .fontSize('24vp')
                  .fontColor([$r('sys.color.ohos_id_color_primary_contrary')])
                  .id('ic_bell_fill')
                  .width('40vp')
                  .height('40vp')
                  .margin({ right: 16 })
                  .draggable(false)
                  .borderRadius(20)
                  .backgroundColor($r('app.color.mms_avatar_bg'))
                  .padding(8)
              }
              Text($r('app.string.infoMessages'))
                .fontSize('16fp')
                .fontColor($r('sys.color.ohos_id_color_text_primary'))
                .fontWeight(FontWeight.Medium)
              Blank()
              if (this.unreadTotalOfInfo > 0) {
                Text(this.unreadTotalOfInfo + '')
                  .height('64vp')
                  .margin({
                    right: $r('app.float.settings_item_status_title_margin_right')
                  })
                  .fontSize($r('app.float.settings_item_secondary_title_font_size'))
                  .fontWeight(FontWeight.Regular)
                  .fontColor($r('sys.color.ohos_id_color_text_secondary'))
                SymbolGlyph($r('sys.symbol.chevron_right'))
                  .width($r('app.float.settings_item_next_image_width'))
                  .height($r('app.float.settings_item_next_image_height'))
                  .fontColor([$r('sys.color.ohos_id_color_fourth')])
                  .draggable(false)
              }
            }
            .width('100%')
            .height('100%')
          }
          .padding({
            left: this.isPC ? 24 : this.isPad ? this.padMargin : 16,
            right: this.isPC ? 24 : this.isPad ? this.padMargin : 16
          })
          .width('100%')
          .height(56)
        }

        LazyForEach(this.searchCtrl.conversationListDataSource, (item: messageType) => {
          ListItem() {
            Row() {
              MmsListItem({
                item: item,
                isMultipleSelectState: this.isMultiSelectStatus,
                isInSetReadThreadIndex: this.isInSetReadThreadIndex,
                loadFromDB: false,
                isPad: this.isPad,
              })
            }
          }
          .width('100%')
          .height(this.fontSizeScale >= 1.45 ? (this.fontSizeScale * 60) + 'vp' : (this.fontSizeScale * 80) + 'vp')
        }, (item: messageType) => JSON.stringify(item))
      }
      .divider({
        strokeWidth: $r('app.float.settings_divider_strokeWidth'),
        startMargin: this.searchCtrl.isShowHead ? (52 + this.padMargin) :
          (this.isPC ? 24 : this.isPad ? this.padMargin : 16),
        endMargin: this.isPC ? 24 : this.isPad ? this.padMargin : 16,
        color: $r('sys.color.ohos_id_color_list_separator')
      })
      .scrollBar(BarState.Off)
    }
    .width('100%')
    .width('100%')
    .backgroundColor($r('sys.color.ohos_id_color_background'))
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/transmitmsg/transmitSearchMsgPage.ets
--- a/entry/src/main/ets/pages/transmitmsg/transmitSearchMsgPage.ets
+++ b/entry/src/main/ets/pages/transmitmsg/transmitSearchMsgPage.ets
@@ -425,6 +425,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct ContentItem {
   item: MySearch = new MySearch();
@@ -494,6 +495,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct ContentListView {
   @Link searchCtrl: TransmitSearchMsgController;
@@ -599,6 +601,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct TransmitSearchEmptyPage {
   build() {


```

## [32/50] ID: OH_0110 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `entry/src/main/ets/pages/dialer/callRecord/InterceptionCalls.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct InterceptionCallView {
  @Link private mPresenter: CallRecordPresenter;

  build() {
    List({ space: 0, initialIndex: 0 }) {
      LazyForEach(this.mPresenter.mInterceptionCallRecordListDataSource, (item: LooseObject, index: number) => {
        ListItem() {
          InterceptionCallItem({ mPresenter: $mPresenter,
            item: item.callLogData,
            index: index,
            showIndex: item.showIndex,
            showDivider: item.showDivider })
        }
      }, (item: LooseObject, index: number) => JSON.stringify(item) + index)
      ListItem() {
      }
      .height('84vp')
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .flexShrink(1)
    .listDirection(Axis.Vertical)
    .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
    .padding({bottom: $r('sys.float.padding_level8') })
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/dialer/callRecord/InterceptionCalls.ets
--- a/entry/src/main/ets/pages/dialer/callRecord/InterceptionCalls.ets
+++ b/entry/src/main/ets/pages/dialer/callRecord/InterceptionCalls.ets
@@ -167,6 +167,7 @@
   }
 }
 
+@Reusable
 @Component
 struct InterceptionCallItem {
   @Link mPresenter: CallRecordPresenter


```

## [33/50] ID: OH_0028 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct RecentList {
  @Link presenter: BatchSelectContactsPresenter;

  build() {
    Column() {
      List({ space: 0, initialIndex: 0 }) {
        LazyForEach(this.presenter.recentSource, (item :BatchSelectContact, index: number) => {
          ListItem() {
            Stack({ alignContent: Alignment.BottomEnd }) {
              BatchSelectRecentItemView({
                item: item.calllog,
                index: item.index,
                onRecentItemClicked: (index: number): void => this.presenter.onRecentItemClicked(index)
              })

              if (item.showDivifer) {
                Divider()
                  .color($r('sys.color.ohos_id_color_list_separator'))
                  .margin({ left: 76, right: $r('app.float.id_card_margin_max') })
              }
            }
          }
        }, (item:BatchSelectContact) => JSON.stringify(item))
      }
      .width('100%')
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring)
    }
    .height('100%')
    .width('100%')
    .backgroundColor(Color.White)
    .padding({ top: $r('app.float.id_card_margin_mid'), bottom: $r('app.float.id_card_margin_mid') })
    .borderRadius($r('sys.float.ohos_id_corner_radius_card'))
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
--- a/entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
+++ b/entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets
@@ -201,6 +201,7 @@
   }
 }
 
+@Reusable
 @Component
 struct RecentList {
   @Link presenter: BatchSelectContactsPresenter;
@@ -238,6 +239,7 @@
   }
 }
 
+@Reusable
 @Component
 struct ContactsList {
   @Link presenter: BatchSelectContactsPresenter;
@@ -317,6 +319,7 @@
   }
 }
 
+@Reusable
 @Component
 struct NoContactsEmptyView {
   @State presenter: BatchSelectContactsPresenter = BatchSelectContactsPresenter.getInstance();


```

## [34/50] ID: OH_0023 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/component/contactdetail/DetailCalllog.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export default struct DetailCalllog {
  @Link private mPresenter: any;

  @Builder callLogTitle() {
    Row() {
      Text($r('app.string.dialer_calllog'))
        .fontSize($r("sys.float.ohos_id_text_size_body1"))
        .fontColor($r("sys.color.ohos_id_color_text_tertiary"))
        .margin({ left: $r("app.float.id_card_margin_max") })

      Blank();

      Text($r('app.string.clear'))
        .fontSize($r("sys.float.ohos_id_text_size_body1"))
        .fontColor($r("sys.color.ohos_id_color_connected"))
        .margin({ right: $r("app.float.id_card_margin_max") })
        .onClick(() => {
          AlertDialog.show({
            message: $r('app.string.clear_calllog_sure'),
            alignment: DialogAlignment.Bottom,
            autoCancel: true,
            primaryButton: {
              value: $r('app.string.dialog_cancel'),
              action: () => {
              }
            },
            secondaryButton: {
              value: $r('app.string.dialog_delete'),
              fontColor: $r("sys.color.ohos_id_color_handup"),
              action: () => {
                this.mPresenter.clearAllCallLog();
              }
            },
            offset: {
              dx: 0, dy: -15
            },
          })
        })
    }
    .width('100%')
    .height($r("app.float.id_item_height_sm"))
  }

  build() {
    Column() {
      List() {
        LazyForEach(this.mPresenter.detailCallLogDataSource, (item, index) => {
          ListItem() {
            Flex({ direction: FlexDirection.Column, justifyContent: FlexAlign.Center, alignItems: ItemAlign.Start }) {
              if ( item.showTitle ) {
                Divider()
                  .strokeWidth(8)
                  .color($r("sys.color.ohos_id_color_subheading_separator"))
                this.callLogTitle()
              }

              CallLogListItem({ message: item.callLog, mPresenter: $mPresenter });
            }
          }
        }, item => item.callLog.id.toString())
      }
      .divider({ strokeWidth: $r("app.float.id_divide_width"),color: $r("sys.color.ohos_id_color_list_separator"),
        startMargin: $r("app.float.id_card_margin_max"), endMargin:$r("app.float.id_card_margin_max")})
    }
    .height("100%")
    .width("100%")
    .backgroundColor(Color.White)
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/component/contactdetail/DetailCalllog.ets
--- a/entry/src/main/ets/component/contactdetail/DetailCalllog.ets
+++ b/entry/src/main/ets/component/contactdetail/DetailCalllog.ets
@@ -21,6 +21,7 @@
 /**
  * Call log
  */
+@Reusable
 @Component
 struct CallLogListItem {
   @State message: any = {};


```

## [35/50] ID: OH_0130 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/index.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let index = 0; index < len; index++) {
      Log.info(TAG,'imageModel START ,this.imageSources '+JSON.stringify(this.imageSources))
      let imageModel = this.imageSources[imageSourceIndexList[index]];
      Log.info(TAG,'imageModel: '+JSON.stringify(imageModel))
      let offCanvas, scale, offCanvasWidth, offCanvasHeight, orientation
      if (this.pageDirection === PageDirection.VERTICAL || (this.pageDirection === PageDirection.AUTO && imageModel.height >= imageModel.width)) {
        //竖向 或者 自适应且图片竖向
        Log.debug('VERTICAL');
        offCanvasWidth = px2fp(size.width);
        offCanvasHeight = px2fp(size.height);
        orientation = PageDirection.VERTICAL
      } else if (this.pageDirection === PageDirection.LANDSCAPE || (this.pageDirection === PageDirection.AUTO && imageModel.height <= imageModel.width)) {
        //横向 自适应且图片横向
        Log.debug('LANDSCAPE');
        offCanvasWidth = px2fp(size.height);
        offCanvasHeight = px2fp(size.width);
        orientation = PageDirection.LANDSCAPE
      } else {
        offCanvasWidth = px2fp(size.width);
        offCanvasHeight = px2fp(size.height);
        Log.error('set offCanvas size error');
      }
      offCanvas = new OffscreenCanvasRenderingContext2D(offCanvasWidth, offCanvasHeight, new RenderingContextSettings(true));
      if (offCanvas === undefined) {
        Log.error(TAG, 'offCanvas is undefined');
        return;
      }
      offCanvas.imageSmoothingEnabled = false;
      offCanvas.fillStyle = '#fff'
      offCanvas.fillRect(Constants.NUMBER_0, Constants.NUMBER_0, offCanvasWidth, offCanvasHeight);
      scale = this.isBorderless ? Math.max(offCanvasWidth / px2fp(imageModel.width), offCanvasHeight / px2fp(imageModel.height)) :
      Math.min(offCanvasWidth / px2fp(imageModel.width), offCanvasHeight / px2fp(imageModel.height));
      let xPosition = (offCanvasWidth - px2fp(imageModel.width * scale)) / Constants.NUMBER_2;
      let yPosition = (offCanvasHeight - px2fp(imageModel.height * scale)) / Constants.NUMBER_2;
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/index.ets
--- a/entry/src/main/ets/pages/index.ets
+++ b/entry/src/main/ets/pages/index.ets
@@ -1317,14 +1317,16 @@
     let size = this.mediaSize.get300PixelMediaSize();
     let fileList = new Array<number>();
     let imageSourceIndexList = new Array<number>();
-    for (let index = 0; index < this.printRange.length; index++) {
-      imageSourceIndexList.push(this.printRange[index] - 1);
+    const printRange = this.printRange;
+    for (let index = 0; index < printRange.length; index++) {
+      imageSourceIndexList.push(printRange[index] - 1);
     }
     Log.info(TAG, 'imageSourceIndexList: ', JSON.stringify(imageSourceIndexList))
     let len = imageSourceIndexList.length;
+    const imageSources = this.imageSources;
     for (let index = 0; index < len; index++) {
-      Log.info(TAG,'imageModel START ,this.imageSources '+JSON.stringify(this.imageSources))
-      let imageModel = this.imageSources[imageSourceIndexList[index]];
+      Log.info(TAG,'imageModel START ,this.imageSources '+JSON.stringify(imageSources))
+      let imageModel = imageSources[imageSourceIndexList[index]];
       Log.info(TAG,'imageModel: '+JSON.stringify(imageModel))
       let offCanvas, scale, offCanvasWidth, offCanvasHeight, orientation
       if (this.pageDirection === PageDirection.VERTICAL || (this.pageDirection === PageDirection.AUTO && imageModel.height >= imageModel.width)) {


```

## [36/50] ID: OH_0025 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct RecordView {
  @Link private mPresenter: CallRecordPresenter;
  @LocalStorageProp('breakpoint') curBp: string = 'sm';
  recordType: number = 0;

  build() {
    List({ space: 0, initialIndex: 0 }) {
      LazyForEach(this.recordType === 0 ? this.mPresenter.mAllCallRecordListDataSource :
      this.mPresenter.mMissCallRecordListDataSource, (item:MergedCallLog, index: number) => {
        ListItem() {
          ContactItem({ mPresenter: mPresenter, item: item, index: index });
        }
        .height($r('app.float.id_item_height_max'))
      }, (item:MergedCallLog) => JSON.stringify(item))
    }
    .divider({
      strokeWidth: 0.5,
      color: $r('sys.color.ohos_id_color_list_separator'),
      startMargin: $r('app.float.id_records_divider_max'),
      endMargin: $r('app.float.id_card_margin_max')
    })
    .width('100%')
    .margin({ bottom: this.curBp === 'lg' ? '110vp' : 0 })
    .flexShrink(1)
    .listDirection(Axis.Vertical)
    .edgeEffect(EdgeEffect.None)
    .scrollBar(BarState.Off)
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets
--- a/entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets
+++ b/entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets
@@ -143,6 +143,7 @@
   sendMessage, Copy, EditBeforeCall, BlockList, DeleteCallLogs, SaveExistingContacts
 }
 
+@Reusable
 @Component
 struct ContactItem {
   @State mIndexPresenter: IndexPresenter = IndexPresenter.getInstance();


```

## [37/50] ID: OH_0116 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `entry/src/main/ets/pages/group/SelectMemberSendMessage.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export default struct SelectMemberSendMessage {
  @Consume('pathInfos') pathInfos: NavPathStack;
  @StorageLink('fullScreenPadding') fullScreenPadding: Padding = {};
  @State mPresenter: SelectMemberSendMessagePresenter = SelectMemberSendMessagePresenter.getInstance();
  @StorageLink('breakpoint') curBp: string = 'sm';
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;
  // 主题字体颜色
  @State mainTitleModifier: MainTitleTextModfier = new MainTitleTextModfier();
  @StorageProp('splitStatus') splitStatus: SplitStatus = SplitStatus.DEFAULT;
  @StorageProp('fontSizeScale') fontSizeScale: number = 0;
  @StorageLink('isShowSmartWindow') isShowSmartWindow: boolean = false;
  private scroller: Scroller = new Scroller();

  aboutToAppear() {
    HiLog.i(TAG, 'aboutToAppear')
    this.mPresenter.pathInfos = this.pathInfos;
    this.mPresenter.aboutToAppear()
  }

  destinationPageShow() {
    HiLog.i(TAG, 'onPageShow')
  }

  destinationPageHide() {
    HiLog.i(TAG, 'onPageCover')
    this.mPresenter.onPageHide()
  }

  destinationBackPress() {
    HiLog.i(TAG, 'onBackPress')
  }

  @Builder
  EmptyPage() {
    Column() {
      // PafEmptyPage({
      //   icon: $r('app.media.ic_empty_page_no_contacts'),
      //   emptyDescription: $r('app.string.no_select_contacts'),
      //   descriptionFontColor: ($r('app.color.skin_font_tertiary')),
      //   fullPage: true,
      //   customBackgroundColor: this.isThemeActive ? Color.Transparent : $r('app.color.skin_background_primary'),
      // })
      Image($r('app.media.ic_empty_page_no_contacts'))
        .objectFit(ImageFit.Contain)
        .width($r('app.float.id_card_image_large'))
        .height($r('app.float.id_card_image_large'))
        .margin({ bottom: $r('app.float.id_card_margin_large') })

      Text($r('app.string.no_select_contacts'))
        .fontSize($r('sys.float.ohos_id_text_size_body2'))
        .fontWeight(FontWeight.Regular)
        .fontColor($r('app.color.skin_font_tertiary'))
        .textAlign(TextAlign.Center)
        .margin({ bottom: $r('app.float.dialer_calllog_item_height') })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  MemberListView() {
    Flex({
      direction: FlexDirection.Column,
      alignItems: ItemAlign.Start,
    }) {
      List({ scroller: this.scroller }) {
        ListItemGroup() {
          LazyForEach(this.mPresenter.groupMemberDataSource, (item: GroupMemberListBean, index?: number |
          undefined) => {
            ListItem() {
              BatchSelectMemberItemView({
                presenter: $mPresenter,
                item: item.member,
                index: item.index,
                onContactItemClicked: (index, indexChild): void =>
                this.mPresenter.onContactItemClicked(index, indexChild),
              })
            }
          }, (item: GroupMemberListBean) => JSON.stringify(item))
        }.divider({
          strokeWidth: 0.3,
          color: $r('app.color.skin_comp_divider'),
          startMargin: 53,
        })
      }
      .width('100%')
      .height('100%')
      .margin({ bottom: $r('app.float.id_toolbar_height') })
      .backgroundColor($r('app.color.skin_background_primary'))
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
      .scrollBar(BarState.Off)
    }
    .padding({
      left: $r('app.float.id_card_margin_max'),
      right: $r('app.float.id_card_margin_max')
    })
  }

  build() {
    NavDestination() {
      Column() {
        GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: { sm: 12, md: 12, lg: 24 }, y: 0 } }) {
          GridCol({ span: { sm: 4, md: 8, lg: 12 } }) {
            Stack({ alignContent: Alignment.Bottom }) {
              if (this.mPresenter.groupMemberDataSource.totalCount() === 0) {
                this.EmptyPage();
              } else {
                this.MemberListView();
              }
              Row() {
                Column() {
                  SymbolGlyph($r('sys.symbol.checkmark'))
                    .fontSize($r('app.float.id_card_image_small'))
                    .fontColor([$r('app.color.skin_icon_primary')])
                    .margin({ bottom: $r('app.float.id_card_margin_sm') })
                    .opacity(this.mPresenter.selectedCount > 0 ? 1 : $r('sys.float.alpha_tertiary'))

                  Text($r('app.string.choose'))
                    .fontColor(this.mPresenter.selectedCount > 0 ? $r('app.color.skin_font_primary') : $r('app.color.skin_font_tertiary'))
                    .fontSize(DisplaySplitUtil.isHorizonSplit(this.splitStatus) ||
                    DisplaySplitUtil.isVerticalSplit(this.splitStatus) ? '10vp' : $r('sys.float.Caption_M'))
                    .fontWeight(FontWeight.Medium)
                }
                .enabled(this.mPresenter.selectedCount > 0 ? true : false)
                .width('50%')
                .height('100%')
                .alignItems(HorizontalAlign.Center)
                .justifyContent(FlexAlign.Center)
                .onClick(() => {
                  this.mPresenter.sendMessage();
                })

                Column() {
                  SymbolGlyph(this.mPresenter.isSelectNumber ?
                    (this.mPresenter.isSelectAll ?
                    $r('sys.symbol.checkmark_square_on_square_fill') : $r('sys.symbol.checkmark_square_on_square'))
                  : $r('sys.symbol.checkmark_square_on_square_fill')
                    )
                    .fontSize($r('app.float.id_card_image_small'))
                    .fontColor(
                    [this.mPresenter.isSelectNumber ? (this.mPresenter.isSelectAll ? $r('app.color.skin_font_emphasize')
                      : $r('app.color.skin_icon_primary')) : $r('app.color.skin_font_tertiary')])

                  Text(this.mPresenter.isSelectNumber ?
                    (this.mPresenter.isSelectAll ? $r('app.string.unselect_all') : $r('app.string.select_all')) :
                  $r('app.string.unselect_all')
                    )
                    .fontColor(this.mPresenter.isSelectNumber ?
                      (this.mPresenter.isSelectAll ?
                      $r('app.color.skin_font_emphasize') : $r('app.color.skin_icon_primary')) :
                     $r('app.color.skin_font_tertiary')
                      )
                    .fontSize(DisplaySplitUtil.isHorizonSplit(this.splitStatus) ||
                    DisplaySplitUtil.isVerticalSplit(this.splitStatus) ? '10vp' : $r('sys.float.Caption_M'))
                    .fontWeight(FontWeight.Medium)
                    .margin({ top: $r('app.float.id_card_margin_sm') })
                }
                .width('50%')
                .height('100%')
                .alignItems(HorizontalAlign.Center)
                .justifyContent(FlexAlign.Center)
                .onClick(() => {
                  this.mPresenter.clickSelectAll();
                })
              }
              .justifyContent(FlexAlign.Center)
              .alignItems(VerticalAlign.Center)
              .width('100%')
              .height(this.fontSizeScale > 5 && this.isShowSmartWindow ? '60vp' : $r('app.float.id_toolbar_height'))
              .padding({
                left: $r('app.float.id_card_margin_max'),
                right: $r('app.float.id_card_margin_max')
              })
            }
          }
        }
      }
      .width('100%')
      .height('100%')
      .backgroundColor($r('app.color.skin_background_primary'))
    }
    .backgroundColor($r('app.color.skin_background_primary'))
    .bindToScrollable([this.scroller])
    // .titleBar(TitleBarUtil.getTitleBar(this.getTitleParam(), undefined, () => {
    //   this.onBack();
    // }))
    .title(this.mPresenter.selectedCount == 0
      ? ResourceUtil.getStringByResource($r('app.string.no_select'))
      : ResourceUtil.getPluralStringByResource($r('app.plural.select_num'), this.mPresenter.selectedCount))
    .onBackPressed(() => {
      this.mPresenter.back();
      return true;
    })
    .onShown(() => {
      this.destinationPageShow();
    })
    .onHidden(() => {
      this.destinationPageHide();
    })
    .padding({
      top:px2vp(this.fullScreenPadding.top as number),
      bottom: px2vp(this.fullScreenPadding.bottom as number)
    })
  }

  private onBack() {
    this.mPresenter.back();
  }

  // private getTitleParam(): TitleBarParams {
  //   return {
  //     avoidLayoutSafeArea: true,
  //     enableComponentSafeArea: true,
  //     title: { title: '', isMultipleSelectState: true, selectedNumber: this.mPresenter.selectedCount },
  //     backIcon: { isThemeActive: this.isThemeActive, backIcon: true }
  //   };
  // }

  @Builder
  selectMemberItemBuilder(item: GroupMemberListBean) {
    BatchSelectMemberItemView({
      presenter: $mPresenter,
      item: item.member,
      index: item.index,
      onContactItemClicked: (index, indexChild): void => this.mPresenter.onContactItemClicked(index, indexChild),
    })
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/group/SelectMemberSendMessage.ets
--- a/entry/src/main/ets/pages/group/SelectMemberSendMessage.ets
+++ b/entry/src/main/ets/pages/group/SelectMemberSendMessage.ets
@@ -276,6 +276,7 @@
   }
 }
 
+@Reusable
 @Component
 struct BatchSelectMemberItemView {
   @Link presenter: SelectMemberSendMessagePresenter;


```

## [38/50] ID: OH_0300 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/changeEncryption.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
this.dlpFile.dlpProperty.authUsers.forEach((item, index) => {
            if (item.authPerm === dlpPermission.AuthPermType.READ_ONLY) {
              this.staffDataArrayReadOnly.push(item);
            } else if (item.authPerm === dlpPermission.AuthPermType.CONTENT_EDIT) {
              this.staffDataArrayEdit.push(item);
            }
          });
```

### Patch
```diff
// File: entry/src/main/ets/pages/changeEncryption.ets
--- a/entry/src/main/ets/pages/changeEncryption.ets
+++ b/entry/src/main/ets/pages/changeEncryption.ets
@@ -425,18 +425,16 @@
                   direction: FlexDirection.Row,
                   wrap: FlexWrap.Wrap,
                 }) {
-                  if (this.staffDataArrayReadOnly['length'] > 0) {
-                    ForEach(
-                      this.staffDataArrayReadOnly,
-                      (item, index) => {
-                        staffItem({
-                          authAccount: item.authAccount,
-                          isActive: false
-                        })
-                      },
-                      (item) => item.authAccount
-                    )
-                  }
+                  ForEach(
+                    this.staffDataArrayReadOnly,
+                    (item, index) => {
+                      staffItem({
+                        authAccount: item.authAccount,
+                        isActive: false
+                      })
+                    },
+                    (item) => item.authAccount
+                  )
                 }.padding({
                   left: Constants.HEADER_COLUMN_PADDING_LEFT,
                   right: Constants.HEADER_COLUMN_PADDING_RIGHT
@@ -484,18 +482,16 @@
                   direction: FlexDirection.Row,
                   wrap: FlexWrap.Wrap,
                 }) {
-                  if (this.staffDataArrayEdit['length'] > 0) {
-                    ForEach(
-                      this.staffDataArrayEdit,
-                      (item, index) => {
-                        staffItem({
-                          authAccount: item.authAccount,
-                          isActive: false
-                        })
-                      },
-                      (item) => item.authAccount
-                    )
-                  }
+                  ForEach(
+                    this.staffDataArrayEdit,
+                    (item, index) => {
+                      staffItem({
+                        authAccount: item.authAccount,
+                        isActive: false
+                      })
+                    },
+                    (item) => item.authAccount
+                  )
                 }.padding({
                   left: Constants.HEADER_COLUMN_PADDING_LEFT,
                   right: Constants.HEADER_COLUMN_PADDING_RIGHT


```

## [39/50] ID: OH_0114 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/ringtoneSelection/RingtoneIndex.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
ListItem() {
                    Column() {
                      this.ringToneItem(item, index);

                      if (index !== (this.ringtoneFullDataList?.ringtoneArray.length - 1)) {
                        Divider()
                          .alignSelf(ItemAlign.Stretch)
                          .strokeWidth('1px')
                          .height($r('app.float.account_Divider_height'))
                          .color($r('sys.color.comp_divider'))
                          .lineCap(LineCapStyle.Square)
                          .padding({ left: $r('sys.float.padding_level4'), right: $r('sys.float.padding_level4') })
                      }
                    }
                    .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])
                    .padding({
                      top: index === 0 ? $r('sys.float.padding_level2') : 0,
                      bottom: index === (this.ringtoneFullDataList?.ringtoneArray.length - 1) ? $r('sys.float.padding_level2') :
                        0,
                      left: $r('sys.float.padding_level2'),
                      right: $r('sys.float.padding_level2'),
                    })
                  }
```

### Patch
```diff
// File: entry/src/main/ets/pages/ringtoneSelection/RingtoneIndex.ets
--- a/entry/src/main/ets/pages/ringtoneSelection/RingtoneIndex.ets
+++ b/entry/src/main/ets/pages/ringtoneSelection/RingtoneIndex.ets
@@ -57,6 +57,79 @@
 
 }
 
+@Reusable
+@Component
+struct RingToneItemComponent {
+  @Prop item: ToneAttrs;
+  @Prop index: number;
+  @Prop ringtoneInfo: RingtoneInfo;
+  onClickRingTone: (item: ToneAttrs) => void = () => {};
+  getRingToneItemTitle: (index: number, item: ToneAttrs) => string = () => '';
+  pressedStyles: () => void = () => {};
+  normalStyles: () => void = () => {};
+
+  @Styles
+  pressedStylesLocal() {
+    .backgroundColor($r('app.color.skin_interactive_click'))
+    .borderRadius($r('sys.float.ohos_id_corner_radius_card'))
+  }
+
+  @Styles
+  normalStylesLocal() {
+    .backgroundColor('rgba(255,255,255,0)')
+  }
+
+  build() {
+    Flex({
+      wrap: FlexWrap.NoWrap,
+      justifyContent: FlexAlign.SpaceBetween,
+      alignItems: ItemAlign.Center
+    }) {
+      Text(this.getRingToneItemTitle(this.index, this.item))
+        .fontFamily('HarmonyHeiTi')
+        .constraintSize({ minHeight: $r('app.float.id_card_image_small') })
+        .fontSize($r('sys.float.Body_L'))
+        .fontColor($r('sys.color.comp_foreground_primary'))
+        .fontWeight(FontWeight.Medium)
+        .textAlign(i18n.isRTL(i18n.System.getSystemLanguage()) ? TextAlign.End : TextAlign.Start)
+        .margin({ end: LengthMetrics.vp(8) })
+        .width(`calc(100% - 32vp)`)
+      if (this.item.uri === this.ringtoneInfo.ringtonePath) {
+        Radio({ value: this.item.title, group: 'radioGroup' })
+          .width($r('app.float.radio_button_width_24'))
+          .constraintSize({ minHeight: $r('app.float.radio_button_width_24') })
+          .margin(0)
+          .padding({
+            top: '2vp',
+            bottom: '2vp',
+            left: '2vp',
+            right: '2vp',
+          })
+          .checked(true)
+          .onChange((isChecked: boolean) => {
+          })
+          .onClick((event) => {
+            HiLog.i(TAG, `onClick`);
+            this.onClickRingTone(this.item);
+          });
+      }
+    }
+    .constraintSize({ minHeight: $r('app.float.id_item_height_mid') })
+    .borderRadius($r('sys.float.corner_radius_level8'))
+    .stateStyles({
+      pressed: this.pressedStylesLocal,
+      normal: this.normalStylesLocal
+    })
+    .padding({ left: $r('sys.float.padding_level4'), right: $r('sys.float.padding_level4') })
+    .onClick(async () => await this.onClickRingTone(this.item))
+    .accessibilityGroup(true)
+    .accessibilityRole(AccessibilityRoleType.RADIO)
+    .accessibilityText(this.getRingToneItemTitle(this.index, this.item))
+    .accessibilityDescription(ResourceUtil.getStringByResource($r('app.string.accessibility_checkbox_deselected')))
+    .accessibilityChecked(this.item.uri === this.ringtoneInfo.ringtonePath)
+  }
+}
+
 /**
  * Ringtone Selection page
  *
@@ -294,53 +367,19 @@
 
   @Builder
   ringToneItem(item: ToneAttrs, index: number): void {
-    Flex({
-      wrap: FlexWrap.NoWrap,
-      justifyContent: FlexAlign.SpaceBetween,
-      alignItems: ItemAlign.Center
-    }) {
-      Text(this.getRingToneItemTitle(index, item))
-        .fontFamily('HarmonyHeiTi')
-        .constraintSize({ minHeight: $r('app.float.id_card_image_small') })
-        .fontSize($r('sys.float.Body_L'))
-        .fontColor($r('sys.color.comp_foreground_primary'))
-        .fontWeight(FontWeight.Medium)
-        .textAlign(i18n.isRTL(i18n.System.getSystemLanguage()) ? TextAlign.End : TextAlign.Start)
-        .margin({ end: LengthMetrics.vp(8) })
-        .width(`calc(100% - 32vp)`)
-      if (item.uri === this.ringtoneInfo.ringtonePath) {
-        Radio({ value: item.title, group: 'radioGroup' })
-          .width($r('app.float.radio_button_width_24'))
-          .constraintSize({ minHeight: $r('app.float.radio_button_width_24') })
-          .margin(0)
-          .padding({
-            top: '2vp',
-            bottom: '2vp',
-            left: '2vp',
-            right: '2vp',
-          })
-          .checked(true)
-          .onChange((isChecked: boolean) => {
-          })
-          .onClick((event) => {
-            HiLog.i(TAG, `onClick`);
-            this.onClickRingTone(item);
-          });
-      }
-    }
-    .constraintSize({ minHeight: $r('app.float.id_item_height_mid') })
-    .borderRadius($r('sys.float.corner_radius_level8'))
-    .stateStyles({
-      pressed: this.pressedStyles,
-      normal: this.normalStyles
-    })
-    .padding({ left: $r('sys.float.padding_level4'), right: $r('sys.float.padding_level4') })
-    .onClick(async () => await this.onClickRingTone(item))
-    .accessibilityGroup(true)
-    .accessibilityRole(AccessibilityRoleType.RADIO)
-    .accessibilityText(this.getRingToneItemTitle(index, item))
-    .accessibilityDescription(ResourceUtil.getStringByResource($r('app.string.accessibility_checkbox_deselected')))
-    .accessibilityChecked(item.uri === this.ringtoneInfo.ringtonePath)
+    RingToneItemComponent({
+      item: item,
+      index: index,
+      ringtoneInfo: this.ringtoneInfo,
+      onClickRingTone: (item: ToneAttrs) => this.onClickRingTone(item),
+      getRingToneItemTitle: (index: number, item: ToneAttrs) => this.getRingToneItemTitle(index, item),
+      pressedStyles: () => {
+        this.pressedStyles()
+      },
+      normalStyles: () => {
+        this.normalStyles()
+      }
+    })
   }
 
   private getRingToneItemTitle(index: number, item: ToneAttrs) {


```

## [40/50] ID: OH_0187 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/PermissionSheet/PermissionStateSheetDialog.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let j = 0; j < reqPermissions.length; j++) {
        let permission = reqPermissions[j];
        if (groups[id].permissions.indexOf(permission) != -1) {
          groupReqPermissions.push(permission);
          this.groupName = groupName;
        }
      }
```

### Patch
```diff
// File: permissionmanager/src/main/ets/PermissionSheet/PermissionStateSheetDialog.ets
--- a/permissionmanager/src/main/ets/PermissionSheet/PermissionStateSheetDialog.ets
+++ b/permissionmanager/src/main/ets/PermissionSheet/PermissionStateSheetDialog.ets
@@ -764,6 +764,8 @@
       Column() {
         List() {
           if (this.currentGroup === 'FOLDER') {
+            const folderStatus = this.folderStatus;
+            const isCheck = this.isCheck;
             ForEach(this.permissions, (permission: Permissions) => {
               ListItem() {
                 Flex({ justifyContent: FlexAlign.Start, alignItems: ItemAlign.Center }) {
@@ -774,7 +776,7 @@
                       .fontWeight(FontWeight.Medium)
                       .flexGrow(Constants.FLEX_GROW)
                     Checkbox()
-                      .select(this.folderStatus[this.getCheckboxInfo(permission).index])
+                      .select(folderStatus[this.getCheckboxInfo(permission).index])
                       .hitTestBehavior(HitTestMode.None)
                   }
                   .width(Constants.FULL_WIDTH)
@@ -790,7 +792,7 @@
               })
               .borderRadius($r('sys.float.ohos_id_corner_radius_default_l'))
               .margin({ top: Constants.TERTIARY_LISTITEM_MARGIN_TOP })
-              .linearGradient((this.isCheck === permission) ? {
+              .linearGradient((isCheck === permission) ? {
                 angle: 90,
                 direction: GradientDirection.Right,
                 colors: [['#DCEAF9', 0.0], ['#FAFAFA', 1.0]]
@@ -812,6 +814,8 @@
               })
             }, (permission: Permissions) => JSON.stringify(permission))
           } else {
+            const selected = this.selected;
+            const isTouch = this.isTouch;
             ForEach(this.mediaDocListItem, (item: MediaDocObj) => {
               ListItem() {
                 Column() {
@@ -824,7 +828,7 @@
                           .fontWeight(FontWeight.Medium)
                           .flexGrow(Constants.FLEX_GROW)
                         Radio({ value: 'Radio', group: 'radioGroup' })
-                          .checked(item.index === this.selected)
+                          .checked(item.index === selected)
                           .hitTestBehavior(HitTestMode.None)
                           .height(Constants.SHAPE_DIA)
                           .width(Constants.SHAPE_DIA)
@@ -843,7 +847,7 @@
                 right: $r('sys.float.ohos_id_card_margin_end')
               })
               .borderRadius($r('sys.float.ohos_id_corner_radius_default_l'))
-              .linearGradient((this.isTouch === item.index) ? {
+              .linearGradient((isTouch === item.index) ? {
                 angle: 90,
                 direction: GradientDirection.Right,
                 colors: [['#DCEAF9', 0.0], ['#FAFAFA', 1.0]]


```

## [41/50] ID: OH_0090 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/hicar/HiCarContactSearchPage.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export default struct HiCarContactSearchPage {
  private static SPACE_8 = 8;
  private static MAX_WIDTH = 448;
  private static EMITTER_ID = 102;
  private contactSearchBoxWidth: number = 0;
  private count: number = 0;
  private guideButtonParams: CustomizedParams = {};
  @State isShowGuide: boolean = true;
  @State inputKeyword: string = '';
  @LocalStorageProp(Constants.KEY_WINDOW_AVOID_AREA_HEIGHT_PX) windowAvoidAreaHeightPx: number = 0;
  @LocalStorageProp(Constants.KEY_WINDOW_AVOID_AREA_WIDTH_PX) windowAvoidAreaWidthPx: number = 0;
  @StorageLink(Constants.KEY_CONTACT_SEARCH_NUMBER) contactSearchNumber: number = 0;

  private getWidth(): number {
    return Math.min(HiCarContactSearchPage.MAX_WIDTH, this.contactSearchBoxWidth);
  }

  private clearSearchResult(): void {
    ContactListPresenter.getInstance().inputKeyword = '';
    // ContactListPresenter.getInstance().getSearchContactResult(ContactListPresenter.getInstance().inputKeyword);
    ContactListPresenter.getInstance().getSearchContactResultFromDb(ContactListPresenter.getInstance().inputKeyword);
  }

  aboutToAppear(): void {
    HiLog.i(TAG, 'HiCarContactSearchPage aboutToAppear.');
    this.clearSearchResult();
    this.contactSearchBoxWidth = HiCarUtil.getInstance().getContactSearchBoxWidth();
    //订阅用户输入为空格时，赋值contactSearchNumber为0
    let innerEvent: emitter.InnerEvent = {
      eventId: HiCarContactSearchPage.EMITTER_ID,
      priority: emitter.EventPriority.HIGH
    };
    emitter.on(innerEvent, (data) => {
      this.contactSearchNumber = data?.data?.['contactSearchCount'];
    });
    //订阅应用当前是不是在手机,当前应用在手机，则不显示当前页面
    const isPhoneEvent: emitter.InnerEvent = {
      eventId: EmitterConstant.EMITTER_NOTICE_WHERE_APP_EVENT_ID,
      priority: emitter.EventPriority.HIGH
    };
    emitter.on(isPhoneEvent, (data) => {
      if (data && this.count < 1) {
        router.back();
        //系统的回调方法会被多次调用，back方法只执行一次
        this.count++;
      }
    });
    sharedPreferencesUtils.init(getContext());
    sharedPreferencesUtils.getFromPreferences(HiCarConstants.KEY_IS_SHOW_GUIDE, true)
      .then(value => {
        this.isShowGuide = value as boolean;
      })
      .catch((error: BusinessError) => {
        HiLog.e(TAG, `Failed to obtain isShowGuide.ERROR: ${error.message}`);
      });
    focusControl.requestFocus('hicar_contactList_contacts_valueChange_search');
  }

  aboutToDisappear(): void {
    HiLog.i(TAG, 'HiCarContactSearchPage aboutToDisappear.');
    this.clearSearchResult();
    emitter.off(HiCarContactSearchPage.EMITTER_ID);
    emitter.off(EmitterConstant.EMITTER_NOTICE_WHERE_APP_EVENT_ID);
  }

  /**
   * 用户初次使用引导界面“我知道”按钮
   */
  @Builder
  okButton() {
    Button() {
      Text($r('app.string.got_it'))
        .fontColor($r('app.color.skin_ohos_id_color_text_primary_activated'))
        .fontSize($r('sys.float.Body_L'))
        .fontWeight(FontWeight.Medium)
    }
    .backgroundColor($r('app.color.skin_ohos_id_color_button_normal'))
    .onClick(() => {
      this.isShowGuide = false;
      sharedPreferencesUtils.saveToPreferences(HiCarConstants.KEY_IS_SHOW_GUIDE, false);
      DotUtil.getInstance().contactDot(this.guideButtonParams, HICAR_SEARCH_GUIDE_KNOW_EVENT);
    })
    .height($r('app.float.id_button_height_hicar'))
    .width(this.getWidth())
    .margin({ bottom: $r('app.float.id_margin_16_hicar') })
  }

  /**
   * 导航的文字内容
   */
  @Builder
  guideText() {
    Text() {
      ForEach(ResourceUtil.resourceToStringById($r('app.string.hua_xiao_fen')).split(''),
        (item: string, index: number) => {
          if (item === 'H' || item === 'X' || item === 'F') {
            Span(item)
              .fontColor($r('app.color.skin_font_emphasize'))
              .fontSize($r('app.float.id_text_size_body1_hicar'))
              .fontWeight(FontWeight.Regular)
          } else {
            Span(item)
              .fontColor($r('app.color.skin_font_tertiary'))
              .fontSize($r('app.float.id_text_size_body1_hicar'))
              .fontWeight(FontWeight.Regular)
          }
        })
    }
    .textAlign(TextAlign.Center)
    .width('100%')
  }

  @Builder
  guideButton() {
    Row({ space: HiCarContactSearchPage.SPACE_8 }) {
      ForEach(['H', 'X', 'F'], (item: string, index: number) => {
        Button({ type: ButtonType.Circle }) {
          Text(item)
            .fontColor($r('app.color.skin_ohos_id_color_text_primary'))
            .fontSize($r('app.float.id_text_size_headline7_hicar'))
            .fontWeight(FontWeight.Medium)
        }
        .width($r('app.float.id_width_48_hicar'))
        .height($r('app.float.id_width_48_hicar'))
        .backgroundColor($r('app.color.skin_ohos_id_color_button_normal'))
      })
    }
    .justifyContent(FlexAlign.Center)
    .margin({ top: $r('app.float.id_margin_8_hicar'), bottom: $r('app.float.id_margin_8_hicar') })
  }

  /**
   * 用户初次使用引导界面
   */
  @Builder
  guideView() {
    Column() {
      Column() {
        Text($r('app.string.initial_and_pinyin_search_supported'))
          .fontColor($r('app.color.skin_ohos_id_color_text_secondary'))
          .fontSize($r('app.float.id_text_size_body1_hicar'))
          .fontWeight(FontWeight.Medium)
          .textAlign(TextAlign.Center)
          .width('100%')
          .margin({ bottom: $r('app.float.id_margin_2_hicar') })

        this.guideText()

        this.guideButton()
      }
      .width('100%')
      .layoutWeight(1)
      .justifyContent(FlexAlign.Center)

      this.okButton()
    }
    .justifyContent(FlexAlign.Center)
    .width('100%')
    .layoutWeight(1)
  }

  /**
   * 搜索组件
   */
  @Builder
  searchBox() {
    Row() {
      Button({ type: ButtonType.Circle }) {
        SymbolGlyph($r('sys.symbol.chevron_backward'))
          .fontSize($r('app.float.id_card_image_small'))
          .fontColor([$r('app.color.skin_ohos_id_color_primary')])
      }
      .onClick(() => {
        router.back();
        this.clearSearchResult();
      })
      .width($r('app.float.id_button_height_hicar'))
      .height($r('app.float.id_button_height_hicar'))
      .margin({ right: $r('app.float.id_margin_8_hicar') })
      .backgroundColor($r('app.color.skin_ohos_id_color_button_normal'))
      .id('hicar_contactList_contacts_back_arrowBack')

      Search({ value: ContactListPresenter.getInstance().inputKeyword, placeholder: $r('app.string.initial_query') })
        .enabled(!this.isShowGuide)
        .layoutWeight(1)
        .searchIcon(new SymbolGlyphModifier($r('sys.symbol.magnifyingglass'))
          .fontColor([$r('app.color.skin_ohos_id_color_secondary')]))
        .cancelButton({ icon: new SymbolGlyphModifier($r('sys.symbol.xmark'))
          .fontColor([$r('app.color.skin_font_tertiary')]) })
        .placeholderColor($r('app.color.skin_font_secondary'))
        .placeholderFont({
          size: ($r('sys.float.Body_L')),
          weight: FontWeight.Regular
        })
        .textFont({ size: $r('sys.float.Body_L') })
        .id('hicar_contactList_contacts_valueChange_search')
        .onChange((value: string) => {
          ContactListPresenter.getInstance().inputKeyword = value;
          // ContactListPresenter.getInstance().getSearchContactResult(ContactListPresenter.getInstance().inputKeyword);
          ContactListPresenter.getInstance().getSearchContactResultFromDb(ContactListPresenter.getInstance().inputKeyword);
          this.inputKeyword = value;
        })
    }
    .height($r('app.float.id_button_height_hicar'))
    .width(this.contactSearchBoxWidth)
    .margin({ top: $r('app.float.id_margin_8_hicar') })
  }

  /**
   * 搜索结果
   */
  @Builder
  contactSearchResultsList() {
    List({ space: 0, initialIndex: 0 }) {
      LazyForEach(ContactListPresenter.getInstance().searchContactsSource, (item: LooseObject, index: number) => {
        ListItem() {
          Column() {
            ContactSearchItem({
              name: item.contact.name.split(new RegExp('<|>', 'gi')),
              contactId: item.contact.entityId
            })
              .width('100%')
              .layoutWeight(1)

            Divider()
              .color($r('app.color.skin_ohos_id_color_list_separator'))
              .strokeWidth('1px')
              .visibility(index === ContactListPresenter.getInstance().searchContactsSource
                .totalCount() - 1 ? Visibility.None : Visibility.Visible)
          }
          .justifyContent(FlexAlign.End)
          .height($r('app.float.id_height_48'))
          .width('100%')
        }
        .id(`HiCarContactSearch_SearchResultClick_ListItem_${index}`)
      }, (item: LooseObject) => JSON.stringify(item))
    }
    .scrollBar(BarState.Off)
  }

  build() {
    Column() {
      this.searchBox()

      if (!this.isShowGuide) {
        if (this.contactSearchNumber > 0) {
          Column() {
            this.contactSearchResultsList()
          }
          .layoutWeight(1)
          .width(this.contactSearchBoxWidth)
          .margin({ top: $r('app.float.id_margin_8_hicar') })
        } else if (this.inputKeyword !== '') {
          Column() {
            BlankPage({ headline: $r('app.string.contact_search_result_empty'), imageType: ImageType.NO_RESULT })
          }
          .justifyContent(FlexAlign.Center)
          .width('100%')
          .layoutWeight(1)
        }
      } else {
        this.guideView()
      }
    }
    .width('100%')
    .height('100%')
    .padding({ left: px2vp(this.windowAvoidAreaWidthPx), bottom: px2vp(this.windowAvoidAreaHeightPx) })
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/hicar/HiCarContactSearchPage.ets
--- a/entry/src/main/ets/pages/hicar/HiCarContactSearchPage.ets
+++ b/entry/src/main/ets/pages/hicar/HiCarContactSearchPage.ets
@@ -309,6 +309,7 @@
   }
 }
 
+@Reusable
 @Component
 struct ContactSearchItem {
   private contactId: number = -1;


```

## [42/50] ID: OH_0262 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `feature/uikit/src/main/ets/component/MenuCustomComponent.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let i = 0; i < result.length; i++) {
      if (result[i] === '%' && result[i + 1] === 's') {
        if (i === 0) {
          this.clickTextPosition = TextClickPosition.START;
          this.start = $r('app.string.location_services');
          this.middle = result.slice(0, i);
          this.end = result.slice(i + 2, result.length);
        } else if (i === (result.length - 1)) {
          this.clickTextPosition = TextClickPosition.END;
          this.start = result.slice(0, i);
          this.middle = result.slice(i + 2, result.length);
          this.end = $r('app.string.location_services');
        } else {
          this.clickTextPosition = TextClickPosition.MIDDLE;
          this.start = result.slice(0, i);
          this.middle = $r('app.string.location_services');
          this.end = result.slice(i + 2, result.length);
        }
        return
      }
    }
```

### Patch
```diff
// File: feature/uikit/src/main/ets/component/MenuCustomComponent.ets
--- a/feature/uikit/src/main/ets/component/MenuCustomComponent.ets
+++ b/feature/uikit/src/main/ets/component/MenuCustomComponent.ets
@@ -230,22 +230,30 @@
     let result = ResourceUtil.getStringSync(resource);
     for (let i = 0; i < result.length; i++) {
       if (result[i] === '%' && result[i + 1] === 's') {
+        let clickTextPosition: string;
+        let start: string | ResourceStr;
+        let middle: string | ResourceStr;
+        let end: string | ResourceStr;
         if (i === 0) {
-          this.clickTextPosition = TextClickPosition.START;
-          this.start = $r('app.string.location_services');
-          this.middle = result.slice(0, i);
-          this.end = result.slice(i + 2, result.length);
+          clickTextPosition = TextClickPosition.START;
+          start = $r('app.string.location_services');
+          middle = result.slice(0, i);
+          end = result.slice(i + 2, result.length);
         } else if (i === (result.length - 1)) {
-          this.clickTextPosition = TextClickPosition.END;
-          this.start = result.slice(0, i);
-          this.middle = result.slice(i + 2, result.length);
-          this.end = $r('app.string.location_services');
+          clickTextPosition = TextClickPosition.END;
+          start = result.slice(0, i);
+          middle = result.slice(i + 2, result.length);
+          end = $r('app.string.location_services');
         } else {
-          this.clickTextPosition = TextClickPosition.MIDDLE;
-          this.start = result.slice(0, i);
-          this.middle = $r('app.string.location_services');
-          this.end = result.slice(i + 2, result.length);
+          clickTextPosition = TextClickPosition.MIDDLE;
+          start = result.slice(0, i);
+          middle = $r('app.string.location_services');
+          end = result.slice(i + 2, result.length);
         }
+        this.clickTextPosition = clickTextPosition;
+        this.start = start;
+        this.middle = middle;
+        this.end = end;
         return
       }
     }
@@ -346,22 +354,30 @@
     let result = ResourceUtil.getStringSync(resource);
     for (let i = 0; i < result.length; i++) {
       if (result[i] === '%' && result[i + 1] === 's') {
+        let clickTextPosition: string;
+        let start: string | ResourceStr;
+        let middle: string | ResourceStr;
+        let end: string | ResourceStr;
         if (i === 0) {
-          this.clickTextPosition = TextClickPosition.START;
-          this.start = $r('app.string.wifi_precision_title');
-          this.middle = result.slice(0, i);
-          this.end = result.slice(i + 2, result.length);
+          clickTextPosition = TextClickPosition.START;
+          start = $r('app.string.wifi_precision_title');
+          middle = result.slice(0, i);
+          end = result.slice(i + 2, result.length);
         } else if (i === (result.length - 1)) {
-          this.clickTextPosition = TextClickPosition.END;
-          this.start = result.slice(0, i);
-          this.middle = result.slice(i + 2, result.length);
-          this.end = $r('app.string.wifi_precision_title');
+          clickTextPosition = TextClickPosition.END;
+          start = result.slice(0, i);
+          middle = result.slice(i + 2, result.length);
+          end = $r('app.string.wifi_precision_title');
         } else {
-          this.clickTextPosition = TextClickPosition.MIDDLE;
-          this.start = result.slice(0, i);
-          this.middle = $r('app.string.wifi_precision_title');
-          this.end = result.slice(i + 2, result.length);
+          clickTextPosition = TextClickPosition.MIDDLE;
+          start = result.slice(0, i);
+          middle = $r('app.string.wifi_precision_title');
+          end = result.slice(i + 2, result.length);
         }
+        this.clickTextPosition = clickTextPosition;
+        this.start = start;
+        this.middle = middle;
+        this.end = end;
         return
       }
     }
@@ -439,22 +455,30 @@
     let result = ResourceUtil.getStringSync(resource);
     for (let i = 0; i < result.length; i++) {
       if (result[i] === '%' && result[i + 1] === 's') {
+        let clickTextPosition: string;
+        let start: string | ResourceStr;
+        let middle: string | ResourceStr;
+        let end: string | ResourceStr;
         if (i === 0) {
-          this.clickTextPosition = TextClickPosition.START;
-          this.start = 'H';
-          this.middle = result.slice(0, i);
-          this.end = result.slice(i + 2, result.length);
+          clickTextPosition = TextClickPosition.START;
+          start = 'H';
+          middle = result.slice(0, i);
+          end = result.slice(i + 2, result.length);
         } else if (i === (result.length - 1)) {
-          this.clickTextPosition = TextClickPosition.END;
-          this.start = result.slice(0, i);
-          this.middle = result.slice(i + 2, result.length);
-          this.end = 'H';
+          clickTextPosition = TextClickPosition.END;
+          start = result.slice(0, i);
+          middle = result.slice(i + 2, result.length);
+          end = 'H';
         } else {
-          this.clickTextPosition = TextClickPosition.MIDDLE;
-          this.start = result.slice(0, i);
-          this.middle = 'H';
-          this.end = result.slice(i + 2, result.length);
+          clickTextPosition = TextClickPosition.MIDDLE;
+          start = result.slice(0, i);
+          middle = 'H';
+          end = result.slice(i + 2, result.length);
         }
+        this.clickTextPosition = clickTextPosition;
+        this.start = start;
+        this.middle = middle;
+        this.end = end;
         return;
       }
     }


```

## [43/50] ID: OH_0013 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 3`
- **Target File:** `entry/src/main/ets/MainAbility/pages/phone/dialer/callRecord/MissedRecord.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct RecordView {
  @Link private mPresenter: CallRecordPresenter;

  build() {
    List() {
      LazyForEach(this.mPresenter.mMissCallRecordListDataSource, (item, index: number) => {
        ListItem() {
          ContactItem({ mPresenter: $mPresenter, item: item });
        }
        .height($r("app.float.dialer_calllog_item_height"))
      }, item => item.id)
    }
    .divider({
      strokeWidth: 1,
      color: $r('sys.color.ohos_id_color_list_separator'),
      startMargin: $r("app.float.id_item_height_sm"),
      endMargin: $r("app.float.id_card_margin_max"),
    })
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/MainAbility/pages/phone/dialer/callRecord/MissedRecord.ets
--- a/entry/src/main/ets/MainAbility/pages/phone/dialer/callRecord/MissedRecord.ets
+++ b/entry/src/main/ets/MainAbility/pages/phone/dialer/callRecord/MissedRecord.ets
@@ -45,6 +45,7 @@
   }
 }
 
+@Reusable
 @Component
 struct RecordView {
   @Link private mPresenter: CallRecordPresenter;
@@ -68,6 +69,7 @@
 }
 
 
+@Reusable
 @Component
 struct EmptyView {
   build() {
@@ -90,6 +92,7 @@
 }
 
 
+@Reusable
 @Component
 struct ContactItem {
   @Link mPresenter: CallRecordPresenter;


```

## [44/50] ID: OH_0234 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/managesim/ManageSim.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export struct ManageSim {
  @Consume('pageInfos') pageInfos: NavPathStack
  @LocalStorageProp('fullScreenPadding') fullScreenPadding: Padding | null = null;
  private context = getContext(this) as myCommon.UIAbilityContext;
  @State mManageSimCtrl: ManageSimController = ManageSimController.getInstance();
  @State mTextInputValue: string = ''
  @State multiSimCard: boolean = MmsPreferences.getInstance().haveMultiSimCardReady();
  dialogController: CustomDialogController = new CustomDialogController({
    builder: LoadingDialog({
      content: $r('app.string.refreshing')
    }),
    autoCancel: true,
  })

  aboutToAppear() {
    this.mManageSimCtrl.onInit(this.pageInfos, this.dialogController)
  }

  /**
   * Triggers once when this page is displayed. In scenarios such as routing and application access to the foreground
   * and background, only customized components modified by @Entry take effect.
   */
  destinationShow() {
    WantUtil.getWant(this.context, this.pageInfos);
  }
  /**
   * Function executes before custom component destructor consumption.
   * Changing state variables in the aboutToDisappear function is not allowed, especially changes to the @Link
   * variable may cause unstable application behavior.
   */
  destinationDisappear() {
    this.mManageSimCtrl.resetList()
  }

  /**
   * Triggered when a user clicks the back button. Only the customized component modified by @Entry takes effect.
   * If true is returned, the page processes the return logic and does not route the page.
   * If false is returned, the default return logic is used.
   * If no value is returned, the value is treated as false.
   */
  onBackPress() {
  }

  build() {
    NavDestination() {
      Column() {
        Stack({ alignContent: Alignment.TopStart }) {
          if (this.mManageSimCtrl.showContent && this.mManageSimCtrl.cardMmsList.length == 0) {
            Column() {
              Flex({ alignItems: ItemAlign.End, justifyContent: FlexAlign.Center }) {
                Column() {
                  Image($rawfile('icon/ic_massage_m.svg'))
                    .width('120vp')
                    .height('120vp')
                    .draggable(false)
                  Text($r('app.string.no_messages'))
                    .fontSize(14)
                    .opacity(0.4)
                    .height(19)
                    .margin({ top: 8 })
                    .fontColor($r('sys.color.font_primary'))
                }.translate({ y: 87 })
              }
              .width('100%')
              .height('40%')
            }
            .width('100%')
            .height('100%')
          }
          // Top Device Title
          Row() {
            SymbolGlyph($r('sys.symbol.chevron_backward'))
              .width($r('app.float.icon_side_length_medium'))
              .height($r('app.float.icon_side_length_medium'))
              .fontColor([$r('sys.color.ohos_id_color_primary')])
              .fontSize('24vp')
              .margin({
                left: $r('app.float.action_bar_margin_left')
              })
              .onClick(() => {
                this.mManageSimCtrl.goBack()
              })
              .draggable(false)
            Row().width($r('app.float.space_16'))
            Text(!this.multiSimCard ? $r('app.string.manage_sim_card_messages') :
              (this.mManageSimCtrl.slotId == 0 ? $r('app.string.manage_sim_card_number_messages', 1) : $r('app.string.manage_sim_card_number_messages', 2)))
              .fontSize($r('app.float.action_bar_text_size'))
              .fontColor($r('sys.color.font_primary'))
              .fontWeight(FontWeight.Medium)
            Row().width('100%').flexShrink(1)
          }
          .width('100%')
          .height($r('app.float.action_bar_height'))
        }
        .height('100%')

        // Content
        Column() {
          if (this.mManageSimCtrl.showContent) {
            if (this.mManageSimCtrl.cardMmsList.length !== 0) {
              Column() {
                List() {
                  LazyForEach(this.mManageSimCtrl.cardMmsListDataSource, (item: LooseObject, index: number) => {
                    ListItem() {
                      Column() {
                        Text(item.name)
                          .textAlign(TextAlign.Start)
                          .fontSize(10)
                          .lineHeight(13)
                          .fontColor($r('sys.color.font_secondary'))
                          .margin({ top: 8, right: 5 })
                        // Message Bubble
                        ManageSimBubbleText({
                          bubbleTextBorderRadius: [4, 24],
                          bubbleTextDirection: 'left',
                          content: item.content,
                          bubbleTextBackgroundColor: $r('sys.color.ohos_id_color_card_bg')
                        })
                          .constraintSize({ maxWidth: 284 })
                          .gesture(
                            TapGesture({ count: 2 })
                              .onAction(() => {
                                this.mManageSimCtrl.pushToCopyController(index);
                              })
                          )
                        Text(item.timeRange)
                          .textAlign(TextAlign.Start)
                          .fontSize(10)
                          .lineHeight(13)
                          .fontColor($r('sys.color.font_secondary'))
                          .margin({ top: 8, right: 5 })
                      }
                      .width('100%')
                      .alignItems(HorizontalAlign.Start)
                      .margin({ bottom: 20 })
                    }.width('100%')
                  }, (item: LooseObject) => JSON.stringify(item))
                }.width('100%')
                .scrollBar(BarState.Off)
                .height('100%')
              }
              .width('100%')
              .height('100%')
            }
          }
        }
        .width('100%')
        .layoutWeight(1)
      }
      .width('100%')
      .height('100%')
      .padding({
        top: this.fullScreenPadding ? (this.fullScreenPadding.top as number) : 0,
        left: $r('app.float.page_padding_left'),
        right: $r('app.float.page_padding_right')
      })
      .backgroundColor($r('sys.color.background_secondary'))
    }
    .onShown(() => {
      this.destinationShow();
    })
    .onDisAppear(() => {
      this.destinationDisappear();
    })
    .hideTitleBar(true)
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/managesim/ManageSim.ets
--- a/entry/src/main/ets/pages/managesim/ManageSim.ets
+++ b/entry/src/main/ets/pages/managesim/ManageSim.ets
@@ -26,6 +26,7 @@
   ManageSim();
 }
 
+@Reusable
 @Component
 export struct ManageSim {
   @Consume('pageInfos') pageInfos: NavPathStack


```

## [45/50] ID: OH_0168 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/pages/authority-tertiary.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let i = 0; i < bundleNames.length; i++) {
      // Get BundleInfo based on bundle name
      bundle.getBundleInfo(bundleNames[i], Constants.PARMETER_BUNDLE_FLAG).then(res => {
        Promise.all([getAppLabel(res.appInfo.labelId, res.name),
          getAppIcon(res.appInfo.iconId, res.name),
          verifyAccessToken(res.appInfo.accessTokenId, routerData[0].permission)])
          .then((values) => {
          this.applicationList[i] = (
            new ApplicationObj(
              String(values[0]),
              String(values[1]),
              i,
              res.appInfo.accessTokenId,
              routerData[0].permission,
              makePy(values[0])[0].slice(0, 1)) // Get the first letter in the returned initials array
          );
          this.oldApplicationItem[i] = (
            new ApplicationObj(
              String(values[0]),
              String(values[1]),
              i,
              res.appInfo.accessTokenId,
              routerData[0].permission,
              makePy(values[0])[0].slice(0, 1)) // Get the first letter in the returned initials array
          );
          // 0: have permission; -1: no permission
          if (values[2] === Constants.PERMISSION_INDEX) {
            this.toggleIsOn[i] = true;
            this.permissionNum++;
          } else {
            this.toggleIsOn[i] = false;
          }
          });
      }).catch(error => {
        console.log(TAG + bundleNames[i] + "getBundleInfo failed, cause: " + JSON.stringify(error));
      })
    }
```

### Patch
```diff
// File: permissionmanager/src/main/ets/pages/authority-tertiary.ets
--- a/permissionmanager/src/main/ets/pages/authority-tertiary.ets
+++ b/permissionmanager/src/main/ets/pages/authority-tertiary.ets
@@ -195,8 +195,9 @@
         this.toggleIsOn[index] = true;
       }
       let num = Constants.PERMISSION_NUM;
-      for(let key in this.toggleIsOn){
-        if(this.toggleIsOn[key]){
+      const toggleIsOnCache = this.toggleIsOn;
+      for(let key in toggleIsOnCache){
+        if(toggleIsOnCache[key]){
           num++;
         }
       }
@@ -226,8 +227,9 @@
         this.toggleIsOn[index] = false;
       }
       let num = Constants.PERMISSION_NUM;
-      for(let key in this.toggleIsOn){
-        if(this.toggleIsOn[key]){
+      const toggleIsOnCache = this.toggleIsOn;
+      for(let key in toggleIsOnCache){
+        if(toggleIsOnCache[key]){
           num++;
         }
       }


```

## [46/50] ID: OH_0178 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `LINTER_FAIL`
- **Target File:** `permissionmanager/src/main/ets/pages/application-secondary.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let j = 0; j < reqPermissions.length; j++) {
        let permission = reqPermissions[j];
        if (groups[id].permissions.indexOf(permission) != -1) {
          groupReqPermissions.push(permission);
        }
      }
```

### Patch
```diff
// File: permissionmanager/src/main/ets/pages/application-secondary.ets
--- a/permissionmanager/src/main/ets/pages/application-secondary.ets
+++ b/permissionmanager/src/main/ets/pages/application-secondary.ets
@@ -272,6 +272,8 @@
   }
 
   build() {
+    const allowedListItem = this.allowedListItem;
+    const bannedListItem = this.bannedListItem;
     Column() {
       GridRow({ gutter: Constants.GUTTER, columns: {
         xs: Constants.XS_COLUMNS, sm: Constants.SM_COLUMNS, md: Constants.MD_COLUMNS, lg: Constants.LG_COLUMNS } }) {
@@ -286,7 +288,7 @@
               }
               Row() {
                 Column() {
-                  if (!this.allowedListItem.length && !this.bannedListItem.length) {
+                  if (!allowedListItem.length && !bannedListItem.length) {
                     Row() {
                       List() {
                         ListItem() {
@@ -323,7 +325,7 @@
                   } else {
                     Scroll() {
                       List() {
-                        if (this.allowedListItem.length) {
+                        if (allowedListItem.length) {
                           ListItem() {
                             Row() {
                               Text($r('app.string.allowed'))
@@ -340,7 +342,7 @@
                           ListItem() {
                             Row() {
                               List() {
-                                ForEach(this.allowedListItem, (item: PermissionObj) => {
+                                ForEach(allowedListItem, (item: PermissionObj) => {
                                   this.ListItemLayout(item, Constants.PERMISSION_ALLOW)
                                 }, (item: PermissionObj) => JSON.stringify(item))
                               }
@@ -360,7 +362,7 @@
                             })
                           }
                         }
-                        if (this.bannedListItem.length) {
+                        if (bannedListItem.length) {
                           ListItem() {
                             Row() {
                               Text($r('app.string.banned'))
@@ -377,7 +379,7 @@
                           ListItem() {
                             Row() {
                               List() {
-                                ForEach(this.bannedListItem, (item: PermissionObj) => {
+                                ForEach(bannedListItem, (item: PermissionObj) => {
                                   this.ListItemLayout(item, Constants.PERMISSION_BAN)
                                 }, (item: PermissionObj) => JSON.stringify(item))
                               }


```

## [47/50] ID: OH_0034 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/contacts/details/ContactDetail.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct Content {
  @Link private mPresenter: DetailPresenter;
  @Link selectSimBuilder: SelectDialogBuilder;
  @LocalStorageProp('breakpoint') curBp: string = 'sm';
  @State colunmHeight: string = '60%';
  @StorageLink('isRouterBack') @Watch('onBackIndex') isRouterBack: boolean = false;

  onBackIndex() {
    if (this.isRouterBack) {
      AppStorage.SetOrCreate('mainTabsIndex', 0);
      router.back();
    }
    this.isRouterBack = false;
  }

  @Builder
  callLogTitle() {
    Row() {
      Text($r('app.string.dialer_calllog'))
        .fontSize($r('sys.float.ohos_id_text_size_body1'))
        .fontColor($r('sys.color.ohos_id_color_text_tertiary'))
        .margin({ left: $r('app.float.id_card_margin_max') })

      Blank();

      Text($r('app.string.clear'))
        .fontSize($r('sys.float.ohos_id_text_size_body1'))
        .fontColor($r('sys.color.ohos_id_color_connected'))
        .margin({ right: $r('app.float.id_card_margin_max') })
        .onClick(() => {
          AlertDialog.show({
            message: $r('app.string.clear_calllog_sure'),
            alignment: EnvironmentProp.isTablet() ? DialogAlignment.Center : DialogAlignment.Bottom,
            autoCancel: true,
            primaryButton: {
              value: $r('app.string.dialog_cancel'),
              action: () => {
              }
            },
            secondaryButton: {
              value: $r('app.string.dialog_delete'),
              fontColor: $r('sys.color.ohos_id_color_handup'),
              action: () => {
                this.mPresenter.clearAllCallLog();
              }
            },
            offset: {
              dx: 0, dy: -15
            },
            gridCount: 4
          })
        })
    }
    .width('100%')
    .height($r('app.float.id_item_height_sm'))
  }

  toPoint(percent: string) {
    let str: string = percent.replace('%', '');
    return Number.parseInt(str) / 100;
  }

  toPercent(point: number) {
    let percent = Number(point * 100).toFixed(4);
    percent += '%';
    return percent;
  }

  build() {
    List() {
      ListItem() {
        Column() {
          Stack({ alignContent: Alignment.Bottom }) {
            Stack()
              .backgroundColor(Color.White)
              .width('100%')
              .height('51vp')
              .borderRadius({ topLeft: 24, topRight: 24 })

            if (this.mPresenter.isNewNumber || this.mPresenter.contactForm.photoFirstName == '-1') {
              Image($r('app.media.ic_user_portrait_morandi'))
                .height('108vp')
                .width('108vp')
                .clip(new Circle({ width: '108vp', height: '108vp' }))
                .border({ width: '4vp', color: Color.White, radius: '100vp' })
                .backgroundColor(this.mPresenter.contactForm.portraitColor)
            } else {
              Text(this.mPresenter.contactForm.photoFirstName)
                .fontSize('40vp')
                .fontWeight(FontWeight.Bold)
                .fontColor(Color.White)
                .height('108vp')
                .width('108vp')
                .textAlign(TextAlign.Center)
                .clip(new Circle({ width: '108vp', height: '108vp' }))
                .border({ width: '4vp', color: Color.White, radius: '100vp' })
                .backgroundColor(this.mPresenter.contactForm.portraitColor)
            }
          }
          .width('100%')
          .height(this.curBp === 'lg' ? '267vp' : '260.5vp')

          Column() {
            Text(this.mPresenter.contactForm.displayName)
              .fontSize('24fp')
              .fontWeight(FontWeight.Medium)
              .margin({ top: '18vp', bottom: '4vp' })
              .width('100%')
              .textAlign(TextAlign.Center)

            Column() {
              if (!StringUtil.isEmpty(this.mPresenter.contactForm.company)) {
                Text(this.mPresenter.contactForm.company)
                  .fontSize($r('sys.float.ohos_id_text_size_body2'))
                  .fontColor($r('sys.color.ohos_id_color_text_tertiary'))
                  .textOverflow({ overflow: TextOverflow.Ellipsis })
                  .maxLines(StringUtil.isEmpty(this.mPresenter.contactForm.position) ? 2 : 1)
              }
              if (!StringUtil.isEmpty(this.mPresenter.contactForm.position)) {
                Text(this.mPresenter.contactForm.position)
                  .fontSize($r('sys.float.ohos_id_text_size_body2'))
                  .fontColor($r('sys.color.ohos_id_color_text_tertiary'))
                  .textOverflow({ overflow: TextOverflow.Ellipsis })
                  .maxLines(1)
              }
            }

            DetailInfoListView({ mPresenter: $mPresenter, selectSimBuilder: $selectSimBuilder });
          }
          .width('100%')
          .backgroundColor(Color.White)
          .padding({ left: $r('app.float.id_card_margin_max'), right: $r('app.float.id_card_margin_max') })

        }
      }
      .onAreaChange((oldArea: Area, newArea: Area) => {
        this.mPresenter.changeTopBarBackgroundColor(newArea.globalPosition.y !== undefined ? newArea.globalPosition.y <= -260 : false)
      })

      ListItemGroup() {
        LazyForEach(this.mPresenter.detailCallLogDataSource, (item: LooseObject, index) => {
          ListItem() {
            Flex({ direction: FlexDirection.Column, justifyContent: FlexAlign.Center, alignItems: ItemAlign.Start }) {
              if (item.showTitle) {
                Divider()
                  .strokeWidth(8)
                  .color($r('sys.color.ohos_id_color_subheading_separator'))
                this.callLogTitle()
              }

              CallLogListItem({ message: item.callLog, mPresenter: $mPresenter });
            }
          }
          .width('100%')
        }, (item: LooseObject) => JSON.stringify(item))
      }
      .backgroundColor(Color.White)
      .onAreaChange((oldArea: Area, newArea: Area) => {
        let itemHeight = AppStorage.Get('windowHeight') == undefined ? 0 :
          (Number(newArea.height) - Number(oldArea.height)) / Number(AppStorage.Get('windowHeight'))
        let itemPoint: number = this.toPoint(this.colunmHeight) - itemHeight;
        this.colunmHeight = itemPoint < 0 ? '0%' : this.toPercent(itemPoint)
      })
      .width('100%')

      ListItem() {
        Column() {
        }
        .height(this.colunmHeight)
        .width('100%')
      }
      .backgroundColor(Color.White)
    }.scrollBar(BarState.Off)
    .edgeEffect(EdgeEffect.None)
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/details/ContactDetail.ets
--- a/entry/src/main/ets/pages/contacts/details/ContactDetail.ets
+++ b/entry/src/main/ets/pages/contacts/details/ContactDetail.ets
@@ -46,6 +46,7 @@
  */
 @Entry(storage)
 @Component
+@Reusable
 struct ContactDetail {
   @State mPresenter: DetailPresenter = DetailPresenter.getInstance();
   @LocalStorageProp('breakpoint') curBp: string = 'sm';
@@ -245,6 +246,7 @@
 }
 
 @Component
+@Reusable
 struct Content {
   @Link private mPresenter: DetailPresenter;
   @Link selectSimBuilder: SelectDialogBuilder;
@@ -426,6 +428,7 @@
  * top bar
  */
 @Component
+@Reusable
 struct TopBar {
   @State hasFavorited: boolean = false;
   @Link private mPresenter: DetailPresenter;


```

## [48/50] ID: OH_0287 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `SECONDARY_DEFECT: 1`
- **Target File:** `entry/src/main/ets/pages/LazyForEachApng.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct LazyForEachApng {
  @State speedRate: number = (router.getParams() as routerParams).speedRate;
  private scrollForList: Scroller = new Scroller();
  private data: SwiperDataSource =
    new SwiperDataSource([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
      26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50])

  build() {
    Column() {
      Row() {
        Button('返回').onClick(() => {
          router.back()
        })
      }

      Column() {
        Text('LazyForEach 加载多个apng图片')
        List({ scroller: this.scrollForList }) {
          LazyForEach(this.data, (item: number) => {
            ListItem() {
              apng({
                src: $r('app.media.stack'),
                speedRate: this.speedRate,
                apngWidth: 200,
                apngHeight: 60
              })
            }
            .height(100).margin({ left: 10, right: 10, top: 10 })
          }, (item: string) => item)
        }
        .width("100%")
        .height("100%")
        .edgeEffect(EdgeEffect.None)
        .friction(0.6)
      }
    }.margin({ left: 16, right: 16 })
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/LazyForEachApng.ets
--- a/entry/src/main/ets/pages/LazyForEachApng.ets
+++ b/entry/src/main/ets/pages/LazyForEachApng.ets
@@ -82,7 +82,7 @@
         List({ scroller: this.scrollForList }) {
           LazyForEach(this.data, (item: number) => {
             ListItem() {
-              apng({
+              ResumApng({
                 src: $r('app.media.stack'),
                 speedRate: this.speedRate,
                 apngWidth: 200,


```

## [49/50] ID: OH_0021 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `LINTER_FAIL`
- **Target File:** `entry/src/main/ets/pages/contacts/ContactList.ets`
- **Warning:** Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct ContactContent {
  @Link private presenter: ContactListPresenter;
  @LocalStorageProp('breakpoint') curBp: string = 'sm';

  @Builder
  GroupsView(imageRes: Resource, title: string | Resource, showArrow: boolean) {
    Row() {
      Row() {
        Image(imageRes)
          .width($r("app.float.id_card_image_mid"))
          .height($r("app.float.id_card_image_mid"))
          .objectFit(ImageFit.Contain)
          .margin({ left: $r("app.float.id_card_margin_max"), right: $r("app.float.id_card_margin_xxl") })

        Text(title)
          .fontSize($r("sys.float.ohos_id_text_size_body1"))
          .fontWeight(FontWeight.Medium)
          .fontColor($r("sys.color.ohos_id_color_text_primary"))
          .layoutWeight(1)
          .textAlign(TextAlign.Start)

        Image($r("app.media.ic_arrow_right_grey"))
          .width(12)
          .height($r("app.float.id_card_image_small"))
          .objectFit(ImageFit.Contain)
          .margin({ right: $r("app.float.id_card_margin_max") })

      }
    }
    .width('100%')
    .height($r("app.float.id_item_height_max"))
    .backgroundColor(Color.White)
  }

  build() {
    Column() {
      GridRow({columns: {sm: 4, md: 8, lg: 12}, gutter: {x: 12, y: 0}}) {
        GridCol({span: {sm: 4, md:6, lg: 8}, offset: {sm: 0, md: 1, lg: 2}}) {
          TitleGuide()
        }

        GridCol({span: {sm: 4, md:6, lg: 8}, offset: {sm: 0, md: 2, lg: 4}}) {
          Column() {
            Text($r("app.string.contact"))
              .fontSize(30)
              .fontWeight(FontWeight.Bold)
              .fontColor($r("sys.color.ohos_id_color_text_primary"))
              .margin({bottom: $r("app.float.id_card_margin_sm")} )
              .lineHeight(42)
              .margin({top:8, bottom: 2})

            Text($r("app.string.contact_num", this.presenter.contactList.length))
              .fontSize($r("sys.float.ohos_id_text_size_body2"))
              .fontWeight(FontWeight.Regular)
              .fontColor($r("sys.color.ohos_id_color_text_tertiary"))
              .lineHeight(19)
          }
          .alignItems(HorizontalAlign.Start)
          .width('100%')
          .height(82)
        }

        GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 2, lg: 4 } }) {
          List({ space: 0, initialIndex: 0 }) {
            LazyForEach(this.presenter.contactListDataSource, (item, index: number) => {
              ListItem() {
                Stack({ alignContent: Alignment.BottomEnd }) {
                  Column() {
                    if (item.showIndex && !StringUtil.isEmpty(item.contact.namePrefix)) {
                      Row() {
                        Text(item.contact.namePrefix)
                          .fontColor($r("sys.color.ohos_fa_text_secondary"))
                          .fontSize($r("sys.float.ohos_id_text_size_sub_title3"))
                          .fontWeight(FontWeight.Medium)
                          .textAlign(TextAlign.Start)
                      }
                      .alignItems(VerticalAlign.Bottom)
                      .direction(Direction.Ltr)
                      .padding({ left: this.curBp === 'lg' ? $r("app.float.id_card_margin_max") : 0,
                         bottom: $r("app.float.id_card_margin_large")})
                      .height($r("app.float.id_item_height_mid"))
                    }

                    ContactListItemView({
                      item: item.contact,
                      index: index,
                      showIndex: item.showIndex,
                      showDivifer: item.showDivifer
                    })
                  }
                  .alignItems(HorizontalAlign.Start)

                  if (item.showDivifer) {
                    Divider()
                      .color($r("sys.color.ohos_id_color_list_separator"))
                      .margin({ right: this.curBp === 'lg' ? 76 : 100,
                        left: this.curBp === 'lg' ? 76 : 100
                      })
                  }
                }
              }
            }, (item) => item.contact.contactId.toString())
          }
          .width('100%')
          .listDirection(Axis.Vertical)
          .edgeEffect(EdgeEffect.Spring)
        }
      }
      .margin({left:24, right:24})
    }
    .height("100%")
    .width("100%")
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/ContactList.ets
--- a/entry/src/main/ets/pages/contacts/ContactList.ets
+++ b/entry/src/main/ets/pages/contacts/ContactList.ets
@@ -65,6 +65,7 @@
   }
 }
 
+@Reusable
 @Component
 struct TitleGuide {
   presenter: ContactListPresenter = ContactListPresenter.getInstance();
@@ -93,6 +94,7 @@
   }
 }
 
+@Reusable
 @Component
 struct ContactContent {
   @Link private presenter: ContactListPresenter;
@@ -209,6 +211,7 @@
   }
 }
 
+@Reusable
 @Component
 export struct ContactEmptyPage {
   @Link presenter: ContactListPresenter;


```

## [50/50] ID: OH_0376 | ArkTS (F)
- **Rule ID:** `@performance/hp-arkui-load-on-demand`
- **Result:** `SECONDARY_DEFECT: 2`
- **Target File:** `entry/src/main/ets/pages/example/thirdpartyscenes/Scene_1.ets`
- **Warning:** Use LazyForEach when appropriate

### Buggy Snippet
```typescript
@Component
struct Scene_1 {
  @State isLoading: boolean = true
  @State animationPaths: string[] = ["common/rlottie/27746-joypixels-partying-face-emoji-animation.json",
    "common/rlottie/29056-nepenthe-illustration.json", "common/rlottie/360_degree.json", "common/rlottie/3d.json",
    "common/rlottie/_alarm.json", "common/rlottie/a_cup_of_coffee.json", "common/rlottie/a_mountain.json",
    "common/rlottie/abstract_circle.json", "common/rlottie/anubis.json", "common/rlottie/ao.json",
    "common/rlottie/balloons_with_string.json", "common/rlottie/bell.json", "common/rlottie/birth_stone_logo.json",
    "common/rlottie/bounching_ball.json", "common/rlottie/browser.json", "common/rlottie/confetti.json",
    "common/rlottie/cooking.json", "common/rlottie/done.json",
    "common/rlottie/dynamic_path_test.json", "common/rlottie/eid_mubarak.json"]
  private controllers: LottieController[] = []
  private scroller: ListScroller = new ListScroller()

  async aboutToAppear() {
    try {
      this.controllers = Array(this.animationPaths.length)
        .fill(null)
        .map(() => new LottieController())
      this.isLoading = false
      lottie.resizeCache(100, 100 * 1024 * 1024);
      lottie.resizeFileCache(100, 100 * 1024 * 1024);
    } catch (error) {
      console.error('Failed to load animations:', error)
    }
  }

  @Builder
  LoadingView() {
    Column() {
      LoadingProgress()
        .width(50)
        .height(50)
      Text('Loading...')
        .fontSize(14)
        .margin({ top: 10 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }

  getFileName(path: string): string {
    return path.split('/').pop()?.replace('.json', '') || ''
  }

  build() {
    Column() {
      if (this.isLoading) {
        this.LoadingView()
      } else {
        List({ space: 5, initialIndex: 4, scroller: this.scroller }) {
          ForEach(this.animationPaths, (path: string, index) => {
            ListItem() {
              Column() {
                LottieView({
                  loop: true,
                  autoplay: true,
                  autoSkip: true,
                  path: $rawfile(path),
                  controller: this.controllers[index],
                })
                  .width('60%')
                  .height('30%')
                  .aspectRatio(1)
                  .backgroundColor('#F1F3F5')
                  .margin(10)
                  .onClick(() => {
                    this.controllers[index].play()
                  })
                Text(this.getFileName(path))
                  .fontSize(14)
                  .margin({ top: 5, bottom: 5 })
                  .textAlign(TextAlign.Center)
                  .maxLines(2)
                  .textOverflow({ overflow: TextOverflow.Ellipsis })
              }
            }
          })
        }
        .height('100%')
        .width('100%')
      }
    }
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/example/thirdpartyscenes/Scene_1.ets
--- a/entry/src/main/ets/pages/example/thirdpartyscenes/Scene_1.ets
+++ b/entry/src/main/ets/pages/example/thirdpartyscenes/Scene_1.ets
@@ -15,6 +15,36 @@
 import { LottieView, LottieController, lottie } from '@ohos/lottie-turbo'
 import common from '@ohos.app.ability.common'
 
+class AnimationDataSource implements IDataSource {
+  private paths: string[] = []
+  private listeners: DataChangeListener[] = []
+
+  constructor(paths: string[]) {
+    this.paths = paths
+  }
+
+  totalCount(): number {
+    return this.paths.length
+  }
+
+  getData(index: number): string {
+    return this.paths[index]
+  }
+
+  registerDataChangeListener(listener: DataChangeListener): void {
+    if (this.listeners.indexOf(listener) < 0) {
+      this.listeners.push(listener)
+    }
+  }
+
+  unregisterDataChangeListener(listener: DataChangeListener): void {
+    const pos = this.listeners.indexOf(listener)
+    if (pos >= 0) {
+      this.listeners.splice(pos, 1)
+    }
+  }
+}
+
 @Entry
 @Component
 struct Scene_1 {
@@ -29,6 +59,7 @@
     "common/rlottie/dynamic_path_test.json", "common/rlottie/eid_mubarak.json"]
   private controllers: LottieController[] = []
   private scroller: ListScroller = new ListScroller()
+  private dataSource: AnimationDataSource = new AnimationDataSource(this.animationPaths)
 
   async aboutToAppear() {
     try {
@@ -68,7 +99,7 @@
         this.LoadingView()
       } else {
         List({ space: 5, initialIndex: 4, scroller: this.scroller }) {
-          ForEach(this.animationPaths, (path: string, index) => {
+          LazyForEach(this.dataSource, (path: string, index: number) => {
             ListItem() {
               Column() {
                 LottieView({
@@ -94,7 +125,7 @@
                   .textOverflow({ overflow: TextOverflow.Ellipsis })
               }
             }
-          })
+          }, (path: string) => path)
         }
         .height('100%')
         .width('100%')


```

