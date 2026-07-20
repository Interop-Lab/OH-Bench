# Oracle Verdict Audit - False Positive (ArkTS)

## [1/50] ID: OH_0280 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `PASS`
- **Target File:** `feature/wifi/src/main/ets/component/WifiPrecisionComponent.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

###  Buggy Snippet
```typescript
for (let i = 0; i < result.length; i++) {
      if (result[i] === '%' && result[i + 1] === 's') {
        if (i === 0) {
          this.clickTextPosition = TextClickPosition.START;
          this.start = $r('app.string.wifi_precision_title');
          this.middle = result.slice(0, i);
          this.end = result.slice(i + SLICE_INDEX, result.length);
        } else if (i === (result.length - 1)) {
          this.clickTextPosition = TextClickPosition.END;
          this.start = result.slice(0, i);
          this.middle = result.slice(i + SLICE_INDEX, result.length);
          this.end = $r('app.string.wifi_precision_title');
        } else {
          this.clickTextPosition = TextClickPosition.MIDDLE;
          this.start = result.slice(0, i);
          this.middle = $r('app.string.wifi_precision_title');
          this.end = result.slice(i + SLICE_INDEX, result.length);
        }
      }
    }
```

### Patch
```diff
// File: feature/wifi/src/main/ets/component/WifiPrecisionComponent.ets
--- a/feature/wifi/src/main/ets/component/WifiPrecisionComponent.ets
+++ b/feature/wifi/src/main/ets/component/WifiPrecisionComponent.ets
@@ -96,26 +96,36 @@
 
   private transFormResource(resource: Resource): void {
     let result = ResourceUtil.getStringSync(resource);
+    let clickTextPosition: string = '';
+    let start: string | ResourceStr = '';
+    let middle: string | ResourceStr = '';
+    let end: string | ResourceStr = '';
+    
     for (let i = 0; i < result.length; i++) {
       if (result[i] === '%' && result[i + 1] === 's') {
         if (i === 0) {
-          this.clickTextPosition = TextClickPosition.START;
-          this.start = $r('app.string.wifi_precision_title');
-          this.middle = result.slice(0, i);
-          this.end = result.slice(i + SLICE_INDEX, result.length);
+          clickTextPosition = TextClickPosition.START;
+          start = $r('app.string.wifi_precision_title');
+          middle = result.slice(0, i);
+          end = result.slice(i + SLICE_INDEX, result.length);
         } else if (i === (result.length - 1)) {
-          this.clickTextPosition = TextClickPosition.END;
-          this.start = result.slice(0, i);
-          this.middle = result.slice(i + SLICE_INDEX, result.length);
-          this.end = $r('app.string.wifi_precision_title');
+          clickTextPosition = TextClickPosition.END;
+          start = result.slice(0, i);
+          middle = result.slice(i + SLICE_INDEX, result.length);
+          end = $r('app.string.wifi_precision_title');
         } else {
-          this.clickTextPosition = TextClickPosition.MIDDLE;
-          this.start = result.slice(0, i);
-          this.middle = $r('app.string.wifi_precision_title');
-          this.end = result.slice(i + SLICE_INDEX, result.length);
+          clickTextPosition = TextClickPosition.MIDDLE;
+          start = result.slice(0, i);
+          middle = $r('app.string.wifi_precision_title');
+          end = result.slice(i + SLICE_INDEX, result.length);
         }
       }
     }
+    
+    this.clickTextPosition = clickTextPosition;
+    this.start = start;
+    this.middle = middle;
+    this.end = end;
   }
 
   aboutToAppear(): void {


```

## [2/50] ID: OH_0050 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/contacts/batchselectcontacts/SingleSelectContactPage.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
```typescript
@Component
struct ContactsList {
  @Link private presenter: BatchSelectContactsPresenter;
  @LocalStorageProp('breakpoint') curBp: string = 'sm';
  private scroller: Scroller = new Scroller();
  @State alphabetSelected: number = 0;
  @State isAlphabetClicked: boolean = false;
  @State dragList: boolean = true;
  @State alphabetIndexPresenter: AlphabetIndexerPresenter = this.presenter.alphabetIndexPresenter;

  build() {
    Column() {
      GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: { sm: 12, md: 12, lg: 24 }, y: 0 } }) {
        GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 1, lg: 2 } }) {
          TitleGuide()
        }
      }
      .onBreakpointChange((breakpoint: string) => {
        this.curBp = breakpoint
      })

      Stack({ alignContent: Alignment.TopEnd }) {
        GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
          GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 1, lg: 2 } }) {
            List({ initialIndex: this.presenter.initialIndex, scroller: this.scroller }) {
              LazyForEach(this.presenter.contactsSource, (item: ContactPickerListItem, index: number) => {
                ListItem() {
                  Stack({ alignContent: Alignment.BottomEnd }) {
                    Column() {
                      if (item.showIndex) {
                        Column() {
                          Text(item.namePrefix)
                            .fontColor($r('sys.color.ohos_fa_text_secondary'))
                            .fontSize($r('sys.float.ohos_id_text_size_sub_title3'))
                            .fontWeight(FontWeight.Medium)
                            .textAlign(TextAlign.Start)
                        }
                        .alignItems(HorizontalAlign.Start)
                        .padding({ left: $r('app.float.id_card_margin_max'), bottom: $r('app.float.id_card_margin_large') })
                        .width('100%')
                        .height($r('app.float.id_item_height_mid'))
                      }
                    }

                    BatchSelectContactItemView({
                      single: true,
                      item: item.contact,
                      index: item.index,
                      onSingleContactItemClick: (num: number,
                        name: string): void => this.presenter.onSingleContactItemClick(num, name, item.contact),
                      showIndex: item.showIndex,
                    })
                  }
                }
              }, (item: ContactPickerListItem) => JSON.stringify(item))
            }
            .scrollBar(BarState.Off)
            .width('100%')
            .listDirection(Axis.Vertical)
            .edgeEffect(EdgeEffect.Spring)
            .onScrollIndex((firstIndex: number, lastIndex: number) => {
              this.presenter.resetInitialIndex(firstIndex);
              if (!this.isAlphabetClicked) {
                this.alphabetSelected = this.alphabetIndexPresenter.getAlphabetSelected(firstIndex);
              }
            })
            .onScrollStart(() => {
              this.dragList = true;
            })
            .onScrollStop(() => {
              this.isAlphabetClicked = false;
            })
          }
        }
        .height('93%')

        AlphabetIndexerPage({
          scroller: this.scroller,
          presenter: $alphabetIndexPresenter,
          selected: this.alphabetSelected,
          isClicked: $isAlphabetClicked,
          drag: $dragList
        })
          .margin({ top: '10%', bottom: '10%' })
      }
      .height('100%')
      .flexShrink(1)
    }
    .width('100%')
    .padding({ top: $r('app.float.id_card_margin_mid'), bottom: $r('app.float.id_card_margin_mid') })
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/batchselectcontacts/SingleSelectContactPage.ets
--- a/entry/src/main/ets/pages/contacts/batchselectcontacts/SingleSelectContactPage.ets
+++ b/entry/src/main/ets/pages/contacts/batchselectcontacts/SingleSelectContactPage.ets
@@ -171,7 +171,7 @@
                     })
                   }
                 }
-              }, (item: ContactPickerListItem) => JSON.stringify(item))
+              }, (item: ContactPickerListItem) => `${item.index}_${item.contact.contactId}`)
             }
             .scrollBar(BarState.Off)
             .width('100%')


```

## [3/50] ID: OH_0012 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/MainAbility/pages/phone/dialer/callRecord/MissedRecord.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
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
@@ -56,7 +56,7 @@
           ContactItem({ mPresenter: $mPresenter, item: item });
         }
         .height($r("app.float.dialer_calllog_item_height"))
-      }, item => item.id)
+      }, item => item.id, { cachedCount: 5 })
     }
     .divider({
       strokeWidth: 1,


```

## [4/50] ID: OH_0330 | ArkTS (T)
- **Rule ID:** `@hw-stylistic/quotes`
- **Result:** `PASS`
- **Target File:** `HMRouterExamples/features/animation_cases/src/main/ets/constants/RouterPageConstant.ets`
- **Warning:** Strings must use single quotes.

###  Buggy Snippet
```typescript
/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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
import { MainPageListItem } from "ui_components";

export class RouterPageConstant {
  static readonly ANIMATOR_MENU: MainPageListItem[] = [
    {
      title: '全局自定义转场',
      pathInfo: { pageUrl: 'animator://globalAnimatorPage' }
    },
    {
      title: '特定页面自定义转场',
      pathInfo: { pageUrl: 'animator://customAnimator' }
    },
    {
      title: '特定页面自定义转场2',
      pathInfo: { pageUrl: 'animator://customAnimator2' }
    },
    {
      title: '特定页面支持交互式(跟手)转场',
      pathInfo: { pageUrl: 'animator://InteractiveAnimator' }
    },
    {
      title: '根据条件选择不同转场',
      pathInfo: { pageUrl: 'animator://OnceAnimator' }
    }
  ];
  static readonly ANIMATOR_TITLE: string = '转场动画配置使用场景';
  static readonly CUSTOM_ANIMATOR_CASE: string = '转场动画使用案例';
  static readonly CUSTOM_ANIMATOR_DESC1: string = '特定页面自定义转场，通过定义@HMRouter中的animator绑定';
  static readonly CUSTOM_ANIMATOR_DESC2: string =
    '特定页面通过customAnimate自定义转场，通过定义@HMRouter中的animator绑定';
}
}
}
}
}
```

### Patch
```diff
// File: HMRouterExamples/features/animation_cases/src/main/ets/constants/RouterPageConstant.ets
--- a/HMRouterExamples/features/animation_cases/src/main/ets/constants/RouterPageConstant.ets
+++ b/HMRouterExamples/features/animation_cases/src/main/ets/constants/RouterPageConstant.ets
@@ -12,7 +12,7 @@
  * See the License for the specific language governing permissions and
  * limitations under the License.
  */
-import { MainPageListItem } from "ui_components";
+import { MainPageListItem } from 'ui_components';
 
 export class RouterPageConstant {
   static readonly ANIMATOR_MENU: MainPageListItem[] = [


```

## [5/50] ID: OH_0117 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/group/SelectMemberSendMessage.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
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
@@ -124,7 +124,7 @@
                 this.mPresenter.onContactItemClicked(index, indexChild),
               })
             }
-          }, (item: GroupMemberListBean) => JSON.stringify(item))
+          }, (item: GroupMemberListBean) => `${item.index}_${item.member.contactId}`)
         }.divider({
           strokeWidth: 0.3,
           color: $r('app.color.skin_comp_divider'),
@@ -436,7 +436,7 @@
               .focusBox({ margin: LengthMetrics.vp(PCDeviceConstant.FOCUS_BOX_MARGIN_NEGATIVE_TWO) })
             }
           }
-        }, (item: PhoneNumberInterface) => JSON.stringify(item))
+        }, (item: PhoneNumberInterface, index: number) => `${item.labelName}_${index}`)
       }
       .listDirection(Axis.Vertical)
       .edgeEffect(EdgeEffect.Spring)


```

## [6/50] ID: OH_0105 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSingleCategoryDetail.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
```typescript
@Component
struct IntelligenceDetailContent {
  @State longPressIndex: number = -1;
  @State isMenuShown: boolean = false;
  @State isPressed: boolean = false;
  @State categoryGroupType: string = '0';
  @Link categoryDetailPresenter: IntelligenceGroupSingleCategoryDetailPresenter;
  @Consume('pathInfos') pathInfos: NavPathStack;
  @StorageLink('breakpoint') curBp: string = 'sm';
  @StorageLink('spaceLR') spaceLR: Resource = $r('sys.float.padding_level8');
  // 字体大小
  @StorageProp('fontSizeScale') fontSizeScale: number = 0;
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;
  @StorageProp('splitStatus') splitStatus: SplitStatus = SplitStatus.DEFAULT;
  private scroller: Scroller = new Scroller();
  nameTitle: string = ContactsGlobalThisHelper.GetGlobalThis()
    .getDefaultUIContext()
    .resourceManager
    .getStringSync($r('app.string.noName').id);
  viewContactDetailParams: CustomizedParams = {
    LEVELONE: 3,
    LEVELTWO: -1,
    ISSAVE: 1,
  };
  customParams: CustomizedParams = {};
  private isPC: boolean = EnvironmentProp.isPC();

  aboutToAppear() {
    HiLog.w(TAG, 'aboutToAppear detail');
  }

  build() {
    GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
      GridCol({ span: { sm: 4, md: 8, lg: 12 } }) {
        List({ scroller: this.scroller }) {
          ListItemGroup({ style: ListItemGroupStyle.CARD }) {
            LazyForEach(this.categoryDetailPresenter.intelligenceGroupListDataSource,
              (item: IntelligenceGroupInfo, index: number) => {
                ListItem() {
                  Flex({
                    direction: FlexDirection.Column,
                    justifyContent: FlexAlign.Center,
                    alignItems: ItemAlign.Start
                  }) {
                    IntelligenceGroupSingleCategoryItem({
                      item: item,
                      categoryDetailPresenter: $categoryDetailPresenter,
                      categoryGroupType: this.categoryGroupType,
                      categoryIndex: index + Constants.EMTPY_STR
                    })
                      .id('IntelligenceGroupCategory_Contacts_LongPressGesture_CategoryGroupItem')
                  }
                  .width('100%')
                }
                .backgroundColor(Color.Transparent)
              }, (item: GroupInfo) => JSON.stringify(item))
          }
          .borderRadius(this.isPC ? '16vp' : $r('sys.float.corner_radius_level10'))
          .margin({
            left: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_left'),
            right: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_right'),
            top: '8vp'
          })
          .backgroundColor($r('sys.color.comp_background_list_card'))
          .divider({
            strokeWidth: '1px',
            startMargin: '8vp',
            endMargin: '8vp',
            color: $r('app.color.skin_ohos_id_color_list_separator'),
          })
          .width('100%')
        }
        .listDirection(Axis.Vertical)
        .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
        .scrollBar(BarState.Off)
        .editMode(true)
        .width('100%')
        .height('100%')
        .backgroundColor(this.isThemeActive ? undefined : $r('app.color.color_bind_sheet_background'))
        .clipContent(ContentClipMode.SAFE_AREA)
        .safeAreaPadding({ top: this.isPC ? 0 : '94vp' })
      }
    }
    .height('100%')
    .flexShrink(1)
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSingleCategoryDetail.ets
--- a/entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSingleCategoryDetail.ets
+++ b/entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSingleCategoryDetail.ets
@@ -275,7 +275,7 @@
                   .width('100%')
                 }
                 .backgroundColor(Color.Transparent)
-              }, (item: GroupInfo) => JSON.stringify(item))
+              }, (item: GroupInfo, index: number) => `${item.groupId ?? ''}_${index}`)
           }
           .borderRadius(this.isPC ? '16vp' : $r('sys.float.corner_radius_level10'))
           .margin({


```

## [7/50] ID: OH_0092 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/hicar/HiCarRecordView.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
```typescript
@Component
export struct HiCarRecordView {
  private scroller: Scroller = new Scroller();
  @Link mPresenter: HiCarCallRecordPresenter;

  build() {
    Column() {
      List({ space: 0, initialIndex: 0, scroller: this.scroller }) {
        LazyForEach(this.mPresenter.mAllCallRecordListDataSource, (item: MergedCallLog, index: number) => {
          ListItem() {
            HiCarCallRecordItem({
              mPresenter: $mPresenter,
              item: item,
              index: index
            })
          }
          .constraintSize({ minHeight: $r('app.float.id_item_height_max') })
          .id(`hicar_record_listItem_${index}`)
          .backgroundColor($r('app.color.skin_background_primary'))
        }, (item: MergedCallLog) => JSON.stringify(item))
      }
      .divider({
        strokeWidth: Constants.DIVIFER_HEIGHT,
        startMargin: $r('app.float.id_margin_24_hicar'),
        endMargin: HiCarUtil.getInstance().getTabContentPadding(),
        color: $r('app.color.skin_ohos_id_color_list_separator')
      })
      .width('100%')
      .height('100%')
      .padding({ left: HiCarUtil.getInstance().getTabContentPadding() })
      .flexShrink(1)
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
      .scrollBar(BarState.Auto)
    }
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/hicar/HiCarRecordView.ets
--- a/entry/src/main/ets/pages/hicar/HiCarRecordView.ets
+++ b/entry/src/main/ets/pages/hicar/HiCarRecordView.ets
@@ -57,7 +57,7 @@
           .constraintSize({ minHeight: $r('app.float.id_item_height_max') })
           .id(`hicar_record_listItem_${index}`)
           .backgroundColor($r('app.color.skin_background_primary'))
-        }, (item: MergedCallLog) => JSON.stringify(item))
+        }, (item: MergedCallLog) => JSON.stringify(item), { cachedCount: 5 })
       }
       .divider({
         strokeWidth: Constants.DIVIFER_HEIGHT,


```

## [8/50] ID: OH_0058 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/group/BatchDeleteGroup.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
```typescript
@Component
export default struct BatchDeleteGroup {
  @Consume('pathInfos') pathInfos: NavPathStack;
  @State @Watch('updateToolbarList') batchDeleteGroupPresenter: BatchDeleteGroupPresenter = BatchDeleteGroupPresenter.getInstance();
  @State mPresenter: GroupListPresenter = GroupListPresenter.getInstance();
  @StorageLink('fullScreenPadding') fullScreenPadding: Padding = {};
  @StorageLink('breakpoint') curBp: string = 'sm';
  @StorageLink('spaceLR') spaceLR: Resource = $r('sys.float.padding_level8');
  //toolbar 数据
  @State toolbarList: ToolBarOptions = new ToolBarOptions()
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;
  // 主题字体颜色
  @State mainTitleModifier: MainTitleTextModfier = new MainTitleTextModfier();
  @StorageProp('isTabletLandscape') isTabletLandscape: boolean = false;
  @StorageProp(AccessibilityUtil.ISOPENACCESSIBILITY) isOpenAccessibility: boolean = false;
  private isPC: boolean = EnvironmentProp.isPC();
  // 是否显示在VisionGlass
  @StorageProp(VisionGlassConstants.KEY_IS_IN_VISION_GLASS) isInVisionGlass: boolean = false;
  private scroller: Scroller = new Scroller();
  // 删除群组按钮、删除群组弹窗参数
  deleteGroupParams: CustomizedParams = {
    NUM: 0,
    ISDELETE: 0
  }

  aboutToAppear() {
    HiLog.w(TAG, 'aboutToAppear');
    this.updateToolbarList();
    this.mPresenter.initNavPaths(this.pathInfos);
    this.batchDeleteGroupPresenter.initNavPaths(this.pathInfos);
    this.batchDeleteGroupPresenter.groupListDataSource = this.mPresenter.groupListDataSource;
    this.batchDeleteGroupPresenter.initGroupData();
    this.batchDeleteGroupPresenter.resetData();
  }

  updateToolbarList() {
    HiLog.w(TAG, 'updateToolbarList');
    this.toolbarList = [];
    this.toolbarList.push({
      content: $r('app.string.delete'),
      toolBarSymbolOptions: {
        normal: new SymbolGlyphModifier($r('sys.symbol.trash')).fontColor([$r('app.color.skin_icon_primary')]),
      },
      state: this.batchDeleteGroupPresenter.selectedCount > 0 ? ItemState.ENABLE : ItemState.DISABLE,
      action: () => {
        this.deleteGroupAction();
      },
    })
  }

  aboutToDisappear() {
    HiLog.w(TAG, 'aboutToDisappear');
    this.batchDeleteGroupPresenter.resetData();
  }

  deleteGroupAction() {
    // 联系人打点--手机群组点击删除群组
    if (this.batchDeleteGroupPresenter.selectedCount === this.batchDeleteGroupPresenter.groupList.length) {
      this.deleteGroupParams.NUM = 2;
    } else if (this.batchDeleteGroupPresenter.selectedCount > 1) {
      this.deleteGroupParams.NUM = 1;
    } else if (this.batchDeleteGroupPresenter.selectedCount === 1) {
      this.deleteGroupParams.NUM = 0;
    } else {
      this.deleteGroupParams.NUM = -1;
    }
    this.deleteGroupParams.ISDELETE = 1;
    DotUtil.getInstance().contactDot(this.deleteGroupParams, DELETE_GROUP_EVENT);
    this.deleteDialogController.open();
    DialogControllerManager.getInstance().addDialogController(this.deleteDialogController);
  }

  // DeleteDialog
  deleteDialogController: CustomDialogController = new CustomDialogController({
    builder: CustomContentDialog({
      theme: this.isThemeActive ? defaultCustomTheme : undefined,
      primaryTitle: this.batchDeleteGroupPresenter.getDeleteDialogTitle(),
      contentBuilder: () => {
        this.DeleteDialogBuilder();
      },
      buttons: [
        {
          value: $r('app.string.cancel'),
          fontColor: this.isThemeActive ? $r('app.color.skin_font_emphasize') : undefined,
          action: () => {
            // 联系人打点--手机群组取消删除群组
            if (this.batchDeleteGroupPresenter.selectedCount === this.batchDeleteGroupPresenter.groupList.length) {
              this.deleteGroupParams.NUM = 2;
            } else if (this.batchDeleteGroupPresenter.selectedCount > 1) {
              this.deleteGroupParams.NUM = 1;
            } else if (this.batchDeleteGroupPresenter.selectedCount === 1) {
              this.deleteGroupParams.NUM = 0;
            } else {
              this.deleteGroupParams.NUM = -1;
            }
            this.deleteGroupParams.ISDELETE = 0;
            DotUtil.getInstance().contactDot(this.deleteGroupParams, GROUP_DELETE_DIALOG_EVENT);
            this.deleteDialogController.close();
            DialogControllerManager.getInstance().dialogControllerSet.clear();
          },
        },
        {
          value: $r('app.string.dialog_delete'),
          action: () => {
            // 联系人打点--手机群组删除群组
            if (this.batchDeleteGroupPresenter.selectedCount === this.batchDeleteGroupPresenter.groupList.length) {
              this.deleteGroupParams.NUM = 2;
            } else if (this.batchDeleteGroupPresenter.selectedCount > 1) {
              this.deleteGroupParams.NUM = 1;
            } else if (this.batchDeleteGroupPresenter.selectedCount === 1) {
              this.deleteGroupParams.NUM = 0;
            } else {
              this.deleteGroupParams.NUM = -1;
            }
            this.deleteGroupParams.ISDELETE = 1;
            DotUtil.getInstance().contactDot(this.deleteGroupParams, GROUP_DELETE_DIALOG_EVENT);
            this.batchDeleteGroupPresenter.deleteEvent();
          },
          role: ButtonRole.ERROR
        }
      ]
    }),
    autoCancel: true,
    backgroundColor: this.isThemeActive ? $r('app.color.skin_ohos_id_color_dialog_bg') : undefined,
    backgroundBlurStyle: this.isPC ? BlurStyle.COMPONENT_ULTRA_THICK :
      this.isThemeActive ? BlurStyle.NONE : undefined,
    shadow: this.isPC ? ShadowStyle.OUTER_DEFAULT_SM : undefined,
    closeAnimation: { duration: 100 }
  });

  // menuItem: Array<HdsNavigationBadgeIconOptions> = [
  //   {
  //     content: {
  //       label: $r('app.string.delete'),
  //       icon: $r('sys.symbol.trash'),
  //       isEnabled: false,
  //     }
  //   }
  // ]
  //
  // menuEnable: Array<HdsNavigationBadgeIconOptions> = [
  //   {
  //     content: {
  //       label: $r('app.string.delete'),
  //       icon: $r('sys.symbol.trash'),
  //       isEnabled: true,
  //       action: () => {
  //         this.deleteGroupAction();
  //       }
  //     }
  //   }
  // ]

  build() {
    NavDestination() {
      Stack({ alignContent: Alignment.Bottom }) {
        Flex({
          direction: FlexDirection.Column,
          alignItems: ItemAlign.Start,
        }) {
          List({ scroller: this.scroller }) {
            ListItem() {
              if (this.isPC) {
                PCSubTitle({ subtitle: $r('app.string.tablet_group') })
              } else {
                SubHeader({
                  secondaryTitle: (this.curBp === 'lg' && !this.isInVisionGlass) ? $r('app.string.tablet_group') :
                  $r('app.string.telep_group'),
                  secondaryTitleModifier: this.isThemeActive ?
                  new TextModifier().fontColor($r('app.color.skin_font_secondary')) : undefined
                })
                  .margin({ left: this.isTabletLandscape ? '-4vp' : $r('app.float.Dialog_bottom'), })
              }
            }

            ListItemGroup() {
              LazyForEach(this.batchDeleteGroupPresenter.groupListDataSource,
                (item: GroupInfo, index?: number | undefined) => {
                  ListItem() {
                    GroupItem({
                      batchDeleteGroupPresenter: $batchDeleteGroupPresenter,
                      item: item,
                      index
                    });
                  }
                }, (item: GroupInfo) => JSON.stringify(item))
            }.divider({
              strokeWidth: 0.3,
              color: $r('app.color.skin_comp_divider'),
            })
            .padding({
              left: this.spaceLR,
              right: this.spaceLR
            })
            .margin({ bottom: $r('app.float.id_card_margin_xxl') })
          }
          .width('100%')
          .height('100%')
          .margin({ bottom: this.isPC ? 0 : $r('app.float.id_item_height_large') })
          .backgroundColor($r('app.color.skin_background_primary'))
          .listDirection(Axis.Vertical)
          .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
          .scrollBar(BarState.Off)
        }

        if (!this.isPC) {
          WithTheme(this.isThemeActive ? { theme: defaultCustomTheme } : undefined) {
            ToolBar({
              activateIndex: this.batchDeleteGroupPresenter.selectedCount ===
              this.batchDeleteGroupPresenter.groupList.length ? 0 : -1,
              dividerModifier: new DividerModifier().height(0),
              toolBarList: this.toolbarList,
            })
              .width('100%')
              .height($r('app.float.id_toolbar_height'))
          }
        }

      }
      .width('100%')
      .height('100%')
      .backgroundColor($r('app.color.skin_background_primary'))
    }
    .bindToScrollable([this.scroller])
    // .titleBar(TitleBarUtil.getTitleBar(this.getTitleParam(), this.isPC ?
    //   (this.batchDeleteGroupPresenter.selectedCount > 0 ? this.menuEnable : this.menuItem) : undefined, () => {
    //   this.onBack();
    // }))
    .title(this.batchDeleteGroupPresenter.selectedCount == 0
      ? ResourceUtil.getStringByResource($r('app.string.no_select'))
      : ResourceUtil.getPluralStringByResource($r('app.plural.select_num'), this.batchDeleteGroupPresenter.selectedCount),
      {
        mainTitleModifier: (this.isThemeActive ? this.mainTitleModifier : undefined),
        paddingStart: this.isPC ? LengthMetrics.vp(16) : undefined,
        paddingEnd:this.isPC ? LengthMetrics.vp(149) : undefined
      })
    .backButtonIcon(this.isThemeActive ?
      new SymbolGlyphModifier($r('sys.symbol.xmark')).fontColor([$r('app.color.skin_icon_primary')])
      :
      new SymbolGlyphModifier($r('sys.symbol.xmark')))
    .onBackPressed(() => {
      this.onBack();
      return true;
    })
    .backgroundColor($r('app.color.skin_background_primary'))
    .padding({
      bottom: this.curBp !== 'sm' ? $r('sys.float.padding_level0') : 50,
      top: px2vp(this.fullScreenPadding.top as number)
    })
  }

  private onBack() {
    // 联系人打点--手机群组点击取消删除群组()
    if (this.batchDeleteGroupPresenter.selectedCount === this.batchDeleteGroupPresenter.groupList.length) {
      this.deleteGroupParams.NUM = 2;
    } else if (this.batchDeleteGroupPresenter.selectedCount > 1) {
      this.deleteGroupParams.NUM = 1;
    } else if (this.batchDeleteGroupPresenter.selectedCount === 1) {
      this.deleteGroupParams.NUM = 0;
    } else {
      this.deleteGroupParams.NUM = -1;
    }
    this.deleteGroupParams.ISDELETE = 0;
    DotUtil.getInstance().contactDot(this.deleteGroupParams, DELETE_GROUP_EVENT);
    this.batchDeleteGroupPresenter.back();
  }

  // private getTitleParam(): TitleBarParams {
  //   return {
  //     avoidLayoutSafeArea: true,
  //     enableComponentSafeArea: true,
  //     padding: {
  //       start: this.isPC ? LengthMetrics.vp(16) : undefined,
  //       end: this.isPC ? LengthMetrics.vp(149) : undefined
  //     },
  //     title: { title: '', isMultipleSelectState: true, selectedNumber: this.batchDeleteGroupPresenter.selectedCount },
  //     backIcon: { isThemeActive: this.isThemeActive, closeIcon: true }
  //   };
  // }

  @Builder
  DeleteDialogBuilder() {
    Scroll() {
      Column() {
        Text($r('app.string.contacts_not_deleted'))
          .fontSize($r('sys.float.Body_L'))
          .fontWeight(FontWeight.Regular)
          .textAlign(this.isPC ? TextAlign.Center : TextAlign.Start)
          .fontColor($r('app.color.skin_font_primary'))
          .width('100%')
          .textAlign(TextAlign.Center)
      }
      .width('100%')
    }
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/group/BatchDeleteGroup.ets
--- a/entry/src/main/ets/pages/group/BatchDeleteGroup.ets
+++ b/entry/src/main/ets/pages/group/BatchDeleteGroup.ets
@@ -235,7 +235,7 @@
                       index
                     });
                   }
-                }, (item: GroupInfo) => JSON.stringify(item))
+                }, (item: GroupInfo) => item.group.id.toString())
             }.divider({
               strokeWidth: 0.3,
               color: $r('app.color.skin_comp_divider'),


```

## [9/50] ID: OH_0329 | ArkTS (T)
- **Rule ID:** `@hw-stylistic/space-before-blocks`
- **Result:** `PASS`
- **Target File:** `HMRouterTransitions/src/main/ets/longTake/LongTakeTransitionDelegate.ets`
- **Warning:** Missing space before opening brace.

###  Buggy Snippet
```typescript
/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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

import { LongTakeSession } from './LongTakeSession';
import { Constants } from '../constants/Constants';
import { image } from '@kit.ImageKit';
import { HMRouterTransitions } from '../HMRouterTransitions';

@Component
export struct LongTakeTransitionDelegate{
  @BuilderParam contentBuilder: () => void;

  @ObjectLink longTakeSession: LongTakeSession;

  @State snapShotImage: image.PixelMap | undefined = undefined;

  aboutToAppear(): void {
    if (this.longTakeSession.snapShotImage) {
      this.snapShotImage = this.longTakeSession.snapShotImage;
    }
  }

  build() {
    Column() {
      Stack({ alignContent: Alignment.TopStart }) {
        // The original content of the popup page, add transparency control for its display during the animation process
        Stack({ alignContent: Alignment.TopStart }) {
          this.contentBuilder()
        }
        .opacity(this.longTakeSession.postPageOpacity)
        .position({ x: this.longTakeSession.positionXValue, y: this.longTakeSession.positionYValue })

        if (this.longTakeSession.snapShotSize) {
          Stack({ alignContent: Alignment.Top }) {
            // Used to display the screenshot of the card clicked on the previous page
            Image(this.snapShotImage)
              .size(this.longTakeSession.snapShotSize)
              .objectFit(ImageFit.Auto)
              .opacity(this.longTakeSession.snapShotOpacity)
}
}
}
}
}
}
```

### Patch
```diff
// File: HMRouterTransitions/src/main/ets/longTake/LongTakeTransitionDelegate.ets
--- a/HMRouterTransitions/src/main/ets/longTake/LongTakeTransitionDelegate.ets
+++ b/HMRouterTransitions/src/main/ets/longTake/LongTakeTransitionDelegate.ets
@@ -19,7 +19,7 @@
 import { HMRouterTransitions } from '../HMRouterTransitions';
 
 @Component
-export struct LongTakeTransitionDelegate{
+export struct LongTakeTransitionDelegate {
   @BuilderParam contentBuilder: () => void;
 
   @ObjectLink longTakeSession: LongTakeSession;


```

## [10/50] ID: OH_0047 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/favorites/favoriteList.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
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
@@ -108,7 +108,7 @@
               ListItem() {
                 FavoriteListItem({ presenter: $mPresenter, item: item, mPresenter: $presenter });
               }
-            }, (item: FavoriteListBean) => JSON.stringify(item))
+            }, (item: FavoriteListBean) => item.favorite.contactId)
           }
           .scrollBar(BarState.Off)
           .editMode(true)


```

## [11/50] ID: OH_0308 | ArkTS (T)
- **Rule ID:** `@previewer/mandatory-default-value-for-local-initialization`
- **Result:** `PASS`
- **Target File:** `TestCases/Demo/product/demo_entry/src/main/ets/components/ListItemComponent.ets`
- **Warning:** If a component attribute supports local initialization, a valid, runtime-independent default value should be set for it.

###  Buggy Snippet
```typescript
@ComponentV2
export struct MainPageListItemComponent {
  @Param @Require pathInfo: HMRouterPathInfo
  @Param callback: HMRouterPathCallback = {}
  @Param @Require description: string

  build() {
    Column({ space: 4 }) {
      Text(this.description).fontSize(14).fontColor('#adb5bd')
      Button('push to: ' + this.pathInfo.pageUrl,
        { controlSize: ControlSize.SMALL, buttonStyle: ButtonStyleMode.TEXTUAL })
        .alignSelf(ItemAlign.End)
        .onClick(() => {
          HMRouterMgr.push(this.pathInfo, this.callback)
        })
    }.alignItems(HorizontalAlign.Start).width('100%').padding({ left: 8, right: 8 })
  }
}
```

### Patch
```diff
// File: TestCases/Demo/product/demo_entry/src/main/ets/components/ListItemComponent.ets
--- a/TestCases/Demo/product/demo_entry/src/main/ets/components/ListItemComponent.ets
+++ b/TestCases/Demo/product/demo_entry/src/main/ets/components/ListItemComponent.ets
@@ -3,7 +3,7 @@
 @ComponentV2
 export struct MainPageListItemComponent {
   @Param @Require pathInfo: HMRouterPathInfo
-  @Param callback: HMRouterPathCallback = {}
+  @Param callback?: HMRouterPathCallback
   @Param @Require description: string
 
   build() {
@@ -13,7 +13,7 @@
         { controlSize: ControlSize.SMALL, buttonStyle: ButtonStyleMode.TEXTUAL })
         .alignSelf(ItemAlign.End)
         .onClick(() => {
-          HMRouterMgr.push(this.pathInfo, this.callback)
+          HMRouterMgr.push(this.pathInfo, this.callback ?? {})
         })
     }.alignItems(HorizontalAlign.Start).width('100%').padding({ left: 8, right: 8 })
   }


```

## [12/50] ID: OH_0377 | ArkTS (T)
- **Rule ID:** `@performance/foreach-args-check`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/example/thirdpartyscenes/Scene_1.ets`
- **Warning:** For performance purposes, set keyGenerator for ForEach.

###  Buggy Snippet
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
@@ -94,7 +94,7 @@
                   .textOverflow({ overflow: TextOverflow.Ellipsis })
               }
             }
-          })
+          }, (path: string) => path)
         }
         .height('100%')
         .width('100%')


```

## [13/50] ID: OH_0236 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-object-link-to-replace-prop`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/conversation/MessageTypeTitleAndCalenderDate.ets`
- **Warning:** Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

###  Buggy Snippet
```typescript
@Component
export default struct MessageTypeTitleAndCalenderDate {
  @Prop mmsItem: mmsListType;

  build() {
    Flex({
      direction: FlexDirection.Column,
      justifyContent: FlexAlign.Center,
      alignItems: ItemAlign.Center
    }) {
      // SMS/MMS
      if (this.mmsItem.showTitle) {
        Text(this.getTitle())
          .fontSize($r('sys.float.Body_S'))
          .lineHeight(16)
          .fontColor($r('sys.color.ohos_id_color_secondary'))
          .margin({ bottom: this.mmsItem.dateShow ? 2 : 16 })
      }
      // Time
      if (this.mmsItem.dateShow) {
        Text() {
          Span(this.mmsItem.dateString)
            .fontSize($r('sys.float.Body_S'))
            .fontColor($r('sys.color.ohos_id_color_secondary'))
        }.lineHeight(16).margin({ bottom: 16 })
      }
    }.width('100%')
  }

  getTitle(): ResourceStr {
    if (this.mmsItem.isIpMsg) {
      return $r('app.string.intelligent_information');
    }
    if (this.mmsItem.isRcs === common.MESSAGE_TYPE.RCS) {
      return $r('app.string.msg_note_rcs');
    }
    return !DeviceUtil.isTablet() ? $r('app.string.msg_note_mms') : '';
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/conversation/MessageTypeTitleAndCalenderDate.ets
--- a/entry/src/main/ets/pages/conversation/MessageTypeTitleAndCalenderDate.ets
+++ b/entry/src/main/ets/pages/conversation/MessageTypeTitleAndCalenderDate.ets
@@ -21,7 +21,7 @@
 
 @Component
 export default struct MessageTypeTitleAndCalenderDate {
-  @Prop mmsItem: mmsListType;
+  @ObjectLink mmsItem: mmsListType;
 
   build() {
     Flex({


```

## [14/50] ID: OH_0041 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/contacts/search/ContactSearch.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
```typescript
@Component
export struct ContactSearch {
  @State batchSelectContactsPresenter: BatchSelectContactsPresenter = BatchSelectContactsPresenter.getInstance();
  @Link presenter: ContactListPresenter;
  @Link type: number;
  @State contactSearchNumber: number = 0;
  emitterId: number = 102;
  @State placeholder: string = '';
  @State cancelIsTouch: boolean = false;

  aboutToAppear() {
    let innerEvent: emitter.InnerEvent = {
      eventId: this.emitterId,
      priority: emitter.EventPriority.HIGH
    };
    emitter.on(innerEvent, (data) => {
      if (data.data !== undefined) {
        this.contactSearchNumber = data.data['contactSearchList'];
      }
    })
  }

  build() {
    Column() {
      GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
        GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 1, lg: 2 } }) {
          Column() {
            Row() {
              Image($r('app.media.ic_public_back'))
                .fillColor($r('sys.color.ohos_id_color_primary'))
                .objectFit(ImageFit.Contain)
                .height($r('app.float.id_card_image_small'))
                .width($r('app.float.id_card_image_small'))
                .onClick(() => {
                  this.presenter.isSearchPage = false;
                  this.presenter.sendEmitter(this.presenter.isSearchPage);
                  this.presenter.inputKeyword = '';
                })

              Stack({ alignContent: Alignment.Center }) {
                TextInput({ text: this.presenter.inputKeyword, placeholder: $r('app.string.contact_list_search') })
                  .placeholderColor(Color.Grey)
                  .placeholderFont({
                    size: $r('sys.float.ohos_id_text_size_headline9'),
                    weight: FontWeight.Normal,
                    style: FontStyle.Normal
                  })
                  .type(InputType.Normal)
                  .caretColor($r('sys.color.ohos_id_color_text_primary_activated'))
                  .enterKeyType(EnterKeyType.Search)
                  .margin({ left: $r('app.float.id_card_image_small'), right: $r('app.float.id_card_image_small') })
                  .padding({ left: $r('app.float.id_card_margin_xxxxl') })
                  .height($r('app.float.id_item_height_mid'))
                  .border({
                    color: $r('sys.color.ohos_id_color_fourth'),
                    radius: $r('app.float.id_card_margin_max')
                  })
                  .onChange((value: string) => {
                    this.presenter.inputKeyword = value
                    this.presenter.getSearchContact(this.presenter.inputKeyword);
                  })
                  .onFocus(() => {
                    focusControl.requestFocus('searchContact');
                  })
                  .id('searchContact')
                  .enableKeyboardOnFocus(true)
                  .defaultFocus(true)

                Flex({ justifyContent: FlexAlign.SpaceBetween, alignItems: ItemAlign.Center }) {
                  Image($r('app.media.ic_public_search'))
                    .width($r('app.float.id_card_margin_xxxl'))
                    .height($r('app.float.id_card_margin_xxxl'))
                    .margin({ left: $r('app.float.id_card_margin_xxxxl') })
                    .objectFit(ImageFit.Contain)

                  if (this.presenter.inputKeyword != '') {
                    Image($r('app.media.ic_public_cancel'))
                      .width($r('app.float.id_card_margin_max'))
                      .height($r('app.float.id_card_margin_max'))
                      .objectFit(ImageFit.Contain)
                      .fillColor($r('sys.color.ohos_id_color_primary'))
                      .opacity(0.6)
                      .margin({ right: $r('app.float.id_card_margin_xxxxl') })
                      .align(Alignment.End)
                      .onClick(() => {
                        this.presenter.inputKeyword = '';
                      })
                  }
                }
                .hitTestBehavior(HitTestMode.Transparent)
              }
              .align(Alignment.Center)
            }
            .padding({ top: $r('app.float.id_card_image_xs'), bottom: $r('app.float.id_card_image_xs') })
            .width('100%')
            .alignItems(VerticalAlign.Center)
            .justifyContent(FlexAlign.Start)
            .align(Alignment.Start)
          }
          .width('100%')
          .backgroundColor(Color.White)
          .padding({ left: $r('app.float.id_card_image_small'), right: $r('app.float.id_card_image_small') })
        }
      }
      .visibility(this.type === 1 || this.type === 2 ? Visibility.None : Visibility.Visible)

      Column() {
        Text($r('app.string.found_contacts', this.contactSearchNumber))
          .fontColor(Color.Gray)
          .margin({ top: $r('app.float.id_card_margin_xxl'), bottom: $r('app.float.id_card_margin_xxl') })
          .width('100%')
          .visibility(this.contactSearchNumber > 0 ? Visibility.Visible : Visibility.None)

        GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
          GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 1, lg: 2 } }) {
            List({ space: 0, initialIndex: 0 }) {
              LazyForEach(this.presenter.searchContactsSource, (item: LooseObject, index: number) => {
                ListItem() {
                  Stack({ alignContent: Alignment.BottomEnd }) {
                    Row() {
                      Row() {
                        if (StringUtil.isEmpty(item?.contact?.photoFirstName)) {
                          Image(StringUtil.isEmpty(item?.contact?.portraitPath) ? $r('app.media.ic_user_portrait') : item?.contact?.portraitPath)
                            .width($r('app.float.id_card_image_mid'))
                            .height($r('app.float.id_card_image_mid'))
                            .objectFit(ImageFit.Contain)
                            .borderRadius($r('app.float.id_card_image_mid'))
                            .backgroundColor(item?.contact?.portraitColor)

                        } else {
                          Text(item?.contact?.photoFirstName.toUpperCase())
                            .fontSize(30)
                            .fontWeight(FontWeight.Bold)
                            .fontColor(Color.White)
                            .backgroundColor(item?.contact?.portraitColor)
                            .height($r('app.float.id_card_image_mid'))
                            .width($r('app.float.id_card_image_mid'))
                            .textAlign(TextAlign.Center)
                            .borderRadius($r('app.float.id_card_image_mid'))
                        }
                      }
                      .height($r('app.float.id_card_image_mid'))
                      .width($r('app.float.id_card_image_mid'))

                      Column() {
                        Row() {
                          ForEach(item?.contact?.displayName.split(this.presenter.inputKeyword), (itemData1: string, idx: number) => {
                            Row() {
                              Text(itemData1.toString())
                                .fontSize($r('sys.float.ohos_id_text_size_body2'))
                                .fontColor($r('sys.color.ohos_id_color_text_tertiary'))
                                .fontWeight(FontWeight.Medium)
                                .margin({ bottom: $r('app.float.id_card_margin_sm') })
                                .textOverflow({ overflow: TextOverflow.Ellipsis })
                                .maxLines(2)
                              if (idx === 0) {
                                if (item?.contact?.displayName.indexOf(this.presenter.inputKeyword) !== -1) {
                                  Text(this.presenter.inputKeyword.toString())
                                    .fontSize($r('sys.float.ohos_id_text_size_body2'))
                                    .fontColor(Color.Blue)
                                    .fontWeight(FontWeight.Medium)
                                    .margin({ bottom: $r('app.float.id_card_margin_sm') })
                                    .textOverflow({ overflow: TextOverflow.Ellipsis })
                                    .maxLines(2)
                                }
                              } else if (item?.contact?.displayName.split(this.presenter.inputKeyword)
                                .length - 1 !== idx) {
                                Text(this.presenter.inputKeyword.toString())
                                  .fontSize($r('sys.float.ohos_id_text_size_body2'))
                                  .fontColor($r('sys.color.ohos_id_color_text_tertiary'))
                                  .fontWeight(FontWeight.Medium)
                                  .margin({ bottom: $r('app.float.id_card_margin_sm') })
                                  .textOverflow({ overflow: TextOverflow.Ellipsis })
                                  .maxLines(2)
                              }
                            }
                          })
                        }

                        Row() {
                          if (!StringUtil.isEmpty(item?.contact?.detailInfo) && '0' !== item?.contact?.hasPhoneNumber) {
                            ForEach(item?.contact?.detailInfo?.split(this.presenter.inputKeyword), (itemData: string, idx: number) => {
                              Row() {
                                Text(itemData.toString())
                                  .fontSize($r('sys.float.ohos_id_text_size_body2'))
                                  .fontColor($r('sys.color.ohos_id_color_text_tertiary'))
                                  .fontWeight(FontWeight.Medium)
                                  .margin({ bottom: $r('app.float.id_card_margin_sm') })
                                  .textOverflow({ overflow: TextOverflow.Ellipsis })
                                  .maxLines(2)
                                if (idx === 0) {
                                  if (item?.contact?.detailInfo.indexOf(this.presenter.inputKeyword) !== -1) {
                                    Text(this.presenter.inputKeyword.toString())
                                      .fontSize($r('sys.float.ohos_id_text_size_body2'))
                                      .fontColor(Color.Blue)
                                      .fontWeight(FontWeight.Medium)
                                      .margin({ bottom: $r('app.float.id_card_margin_sm') })
                                      .textOverflow({ overflow: TextOverflow.Ellipsis })
                                      .maxLines(2)
                                  }
                                } else if (item?.contact?.detailInfo.split(this.presenter.inputKeyword)
                                  .length - 1 !== idx) {
                                  Text(this.presenter.inputKeyword.toString())
                                    .fontSize($r('sys.float.ohos_id_text_size_body2'))
                                    .fontColor($r('sys.color.ohos_id_color_text_tertiary'))
                                    .fontWeight(FontWeight.Medium)
                                    .margin({ bottom: $r('app.float.id_card_margin_sm') })
                                    .textOverflow({ overflow: TextOverflow.Ellipsis })
                                    .maxLines(2)
                                }
                              }
                            })
                          }
                        }
                      }
                      .alignItems(HorizontalAlign.Start)
                      .padding({
                        top: $r('app.float.id_card_margin_mid'),
                        bottom: $r('app.float.id_card_margin_mid'),
                      })
                      .margin({ left: $r('app.float.id_card_margin_xl') })
                    }
                    .constraintSize({ minHeight: $r('app.float.id_item_height_max') })
                    .width('100%')
                    .height($r('app.float.id_item_height_large'))

                    Divider()
                      .color($r('sys.color.ohos_id_color_list_separator'))
                      .visibility(this.contactSearchNumber > 1 && this.contactSearchNumber - item.index > 1 ? Visibility.Visible : Visibility.None)
                      .margin({
                        left: $r('app.float.id_item_height_large'),
                        right: $r('app.float.id_card_image_small')
                      })
                  }
                }
                .onClick(() => {
                  if (this.type === 0) {
                    router.pushUrl(
                      {
                        url: 'pages/contacts/details/ContactDetail',
                        params: {
                          sourceHasId: true,
                          contactId: item.contact.contactId
                        }
                      }
                    );
                  } else if (this.type === 1) {
                    this.batchSelectContactsPresenter.onSingleContactItemClick(0, item.contact.displayName, item.contact.contactId);
                  } else if (this.type === 2) {
                  }
                })
              }, (item: ContactPickerListItem) => JSON.stringify(item))
            }
            .height('90%')
            .width('100%')
            .listDirection(Axis.Vertical)
          }
        }
        .height('100%')
        .flexShrink(1)
      }
      .height('100%')
      .width('100%')
      .padding({ left: this.type === 0 && this.contactSearchNumber > 0 ? $r('app.float.id_card_image_small') : 0 })
      .visibility(this.contactSearchNumber > 0 && !this.presenter.isSearchBackgroundColor ? Visibility.Visible : Visibility.None)

      ContactSearchEmptyPage({ contactSearchNumber: $contactSearchNumber, presenter: $presenter, type: $type });
    }
    .padding({ bottom: $r('app.float.dialer_calllog_item_height') })
    .height('100%')
    .width('100%')
    .backgroundColor(this.type === 1 || this.type === 2 ? $r('sys.color.ohos_id_color_sub_background') :
      this.type === 0 && this.contactSearchNumber > 0 ? Color.White : '#450a0a0a')
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/search/ContactSearch.ets
--- a/entry/src/main/ets/pages/contacts/search/ContactSearch.ets
+++ b/entry/src/main/ets/pages/contacts/search/ContactSearch.ets
@@ -272,7 +272,7 @@
                   } else if (this.type === 2) {
                   }
                 })
-              }, (item: ContactPickerListItem) => JSON.stringify(item))
+              }, (item: ContactPickerListItem) => item.contact.contactId.toString())
             }
             .height('90%')
             .width('100%')


```

## [15/50] ID: OH_0257 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `PASS`
- **Target File:** `product/phone/src/main/ets/Setting/IntelligentScene/view/AppSelectedGroupsComponent.ets`
- **Warning:** Use reusable components to define complex components whenever possible

###  Buggy Snippet
```typescript
@Component
export struct AppSelectedGroupsComponent {
  private onAppItemClicked: (index: number, item: AppInfo) => void = () => {};
  @Link appGroups: AppInfoDataSource;

  build() {
    Column() {
      List({ space: 0, initialIndex: 0 }) {
        LazyForEach(this.appGroups, (item: AppInfo, index: number) => {
          ListItem() {
            AppListDataInfoComponent({
              item: item,
              index: index,
              totalCount: this.appGroups.totalCount(),
              onAppItemClicked: this.onAppItemClicked,
              isSelectedList: true,
            })
          }
        }, (item: AppInfo) => (`${item.name}${item.isSelected}`))
      }
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring)
      .scrollBar(BarState.Off)
    }
  }
}
```

### Patch
```diff
// File: product/phone/src/main/ets/Setting/IntelligentScene/view/AppSelectedGroupsComponent.ets
--- a/product/phone/src/main/ets/Setting/IntelligentScene/view/AppSelectedGroupsComponent.ets
+++ b/product/phone/src/main/ets/Setting/IntelligentScene/view/AppSelectedGroupsComponent.ets
@@ -23,24 +23,31 @@
   private onAppItemClicked: (index: number, item: AppInfo) => void = () => {};
   @Link appGroups: AppInfoDataSource;
 
+  @Builder
+  buildListItem(item: AppInfo, index: number) {
+    AppListDataInfoComponent({
+      item: item,
+      index: index,
+      totalCount: this.appGroups.totalCount(),
+      onAppItemClicked: this.onAppItemClicked,
+      isSelectedList: true,
+    })
+  }
+
   build() {
     Column() {
       List({ space: 0, initialIndex: 0 }) {
         LazyForEach(this.appGroups, (item: AppInfo, index: number) => {
           ListItem() {
-            AppListDataInfoComponent({
-              item: item,
-              index: index,
-              totalCount: this.appGroups.totalCount(),
-              onAppItemClicked: this.onAppItemClicked,
-              isSelectedList: true,
-            })
+            this.buildListItem(item, index)
           }
+          .reuseId('appListItem')
         }, (item: AppInfo) => (`${item.name}${item.isSelected}`))
       }
       .listDirection(Axis.Vertical)
       .edgeEffect(EdgeEffect.Spring)
       .scrollBar(BarState.Off)
+      .cachedCount(5)
     }
   }
 }


```

## [16/50] ID: OH_0163 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-object-link-to-replace-prop`
- **Result:** `PASS`
- **Target File:** `CertManager/src/main/ets/pages/trustedCa.ets`
- **Warning:** Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

###  Buggy Snippet
```typescript
@Component
export struct TrustedEvidence {
  @State mShowSysCaPresenter: CmShowSysCaPresenter = CmShowSysCaPresenter.getInstance();
  @State mShowUserCaPresenter: CMShowUserCaPresenter = CMShowUserCaPresenter.getInstance();
  @State mFaPresenter: CmFaPresenter = CmFaPresenter.getInstance();
  @State currentIndex: number = 0;
  @State fontColor: Resource = $r('app.color.TrustedEvidence_TabBuilder_fontColor_182431');
  @State selectedFontColor: Resource = $r('app.color.font_color_007DFF');
  private controller: TabsController = new TabsController();
  private sysCaScroller: Scroller = new Scroller();
  private userCaScroller: Scroller = new Scroller();
  @State animationDurationNum: number = 400;

  isStartBySheetFirst: boolean = false;
  isStartBySheet: boolean = false;
  selected?: (path: string, param?: Object) => void;
  @Prop sheetParam: SheetParam;
  @State headRectHeight: number = 64;
  @State headRectHeightReal: number = 0;
  @State private sysScrollerHeight: number = 0;
  @State private userScrollerHeight: number = 0;

  @Builder
  TabBuilder(index: number) {
    Column() {
      Text(index == 0 ? $r('app.string.system') : $r('app.string.user'))
        .fontColor(this.currentIndex === index ? this.selectedFontColor : this.fontColor)
        .fontSize($r('app.float.TrustedEvidence_TabBuilder_Text_fontSize_value'))
        .fontWeight(this.currentIndex === index ? FontWeight.Medium : FontWeight.Regular)
        .alignSelf(ItemAlign.Center)
        .margin({
          top: $r('app.float.TrustedEvidence_TabBuilder_Text_padding_top_value')
        })
      if (this.currentIndex === index) {
        Divider()
          .width($r('app.float.TrustedEvidence_TabBuilder_Divider_width_value'))
          .margin({ top: $r('app.float.TrustedEvidence_TabBuilder_Divider_padding_top_value') })
          .color(this.selectedFontColor)
          .alignSelf(ItemAlign.Center)
      }
    }
    .width(WidthPercent.WH_100_100)
  }

  aboutToAppear() {
    this.mShowSysCaPresenter.updateSystemTrustedCertificateList();
    this.mShowUserCaPresenter.updateUserTrustedCertificateList();
  }

  onPageShow() {
    let uri = GlobalContext.getContext().getAbilityWant().uri;
    GlobalContext.getContext().clearAbilityWantUri();

    if (uri === 'certInstall') {
      router.pushUrl({
        url: 'pages/certInstallFromStorage'
      })
    } else if (uri === 'requestAuthorize') {
      this.mFaPresenter.startRequestAuth(GlobalContext.getContext().getAbilityWant().parameters?.appUid as string);
    } else {
      console.error('The want type is not supported');
    }
  }

  build() {
    Column() {
      GridRow({ columns: COPIES_NUM, gutter: vp2px(1) === 2 ? $r('app.float.wh_value_12') : $r('app.float.wh_value_0') }) {
        GridCol({ span: COPIES_NUM }) {
          Row() {
            Stack({ alignContent: Alignment.Top }) {
              Column() {
                HeadComponent({ headName: $r('app.string.CA_cert'), isStartBySheet: this.isStartBySheet,
                  icBackIsVisibility: !this.isStartBySheetFirst,
                  onBackClicked: () => {
                    this.selected?.(NavEntryKey.POP);
                  }})
                  .margin({
                    left: $r('app.float.wh_value_12'),
                    top: this.isStartBySheet ? 8 : 0
                  })
              }.onAreaChange((oldArea, newArea) => {
                this.headRectHeight = newArea.height as number;
                this.headRectHeightReal = newArea.height as number;
              }).zIndex(1)

              Column() {
                Tabs({ barPosition: BarPosition.Start, index: 0, controller: this.controller }) {
                  TabContent() {
                    Stack({ alignContent: Alignment.TopEnd }) {
                      Scroll(this.sysCaScroller) {
                        List() {
                          ForEach(this.mShowSysCaPresenter.certList, (item: CertAbstractVo) => {
                            ListItem() {
                              ComponentSystem({
                                certAlias: item.certAlias,
                                subjectName: item.subjectNameCN,
                                uri: item.uri,
                                setStatus: $mShowSysCaPresenter,
                                onItemClicked: this.isStartBySheet ? () => {
                                  this.selected?.(NavEntryKey.CA_SYSTEM_DETAIL_ENTRY);
                                } : undefined
                              })
                            }
                          }, (item: CertAbstractVo) => JSON.stringify(item))
                        }
                        .borderRadius($r('sys.float.padding_level10'))
                        .backgroundColor($r('sys.color.ohos_id_color_card_bg'))
                        .scrollBar(BarState.Off)
                        .padding({
                          right: $r('app.float.wh_value_4'),
                          left: $r('app.float.wh_value_4'),
                          top: $r('app.float.wh_value_4'),
                          bottom: $r('app.float.wh_value_4')
                        })
                        .divider({
                          strokeWidth: $r('app.float.sys_list_divider_strokeWidth_value'),
                          color: $r('sys.color.ohos_id_color_list_separator'),
                          startMargin: $r('app.float.wh_value_8'),
                          endMargin: $r('app.float.wh_value_8')
                        })
                        .visibility(this.mShowSysCaPresenter.certList.length > 0
                          ? Visibility.Visible : Visibility.None)
                      }
                      .width(WidthPercent.WH_100_100)
                      .height(this.isStartBySheet ? WidthPercent.WH_AUTO : WidthPercent.WH_100_100)
                      .align(Alignment.Top)
                      .edgeEffect(EdgeEffect.Spring)
                      .scrollable(ScrollDirection.Vertical)
                      .scrollBar(BarState.Off)
                      .padding({
                        left: $r('app.float.wh_value_16'),
                        right: $r('app.float.wh_value_16'),
                        bottom: this.isStartBySheet ? $r('app.float.wh_value_80') : $r('app.float.wh_value_24')
                      })
                      .constraintSize({
                        minHeight: this.getScrollMinHeight()
                      }).onAreaChange((oldArea, newArea) => {
                        this.sysScrollerHeight = newArea.height as number;
                      })

                      Column() {
                        ScrollBar({
                          scroller: this.sysCaScroller,
                          direction: ScrollBarDirection.Vertical,
                          state: BarState.Auto
                        }).margin({
                          bottom: this.isStartBySheet ? $r('app.float.wh_value_80') : $r('app.float.wh_value_24')
                        })
                      }.height(this.sysScrollerHeight)
                    }
                  }
                  .tabBar(this.TabBuilder(0))

                  TabContent() {
                    Stack({ alignContent: Alignment.TopEnd }) {
                      Scroll(this.userCaScroller) {
                        List() {
                          ForEach(this.mShowUserCaPresenter.certList, (item: CertAbstractVo, index) => {
                            ListItem() {
                              ComponentUser({
                                certAlias: item.certAlias,
                                subjectName: item.subjectNameCN,
                                uri: item.uri,
                                setStatus: $mShowUserCaPresenter,
                                indexNum: index,
                                onItemClicked: this.isStartBySheet ? () => {
                                  this.selected?.(NavEntryKey.CA_USER_DETAIL_ENTRY,
                                    new CaUserDetailParam(this.mShowUserCaPresenter));
                                } : undefined
                              })
                            }
                          }, (item: CertAbstractVo) => JSON.stringify(item))
                        }
                        .borderRadius($r('sys.float.padding_level10'))
                        .backgroundColor($r('sys.color.ohos_id_color_card_bg'))
                        .divider({
                          strokeWidth: $r('app.float.sys_list_divider_strokeWidth_value'),
                          color: $r('sys.color.ohos_id_color_list_separator'),
                          startMargin: $r('app.float.wh_value_8'),
                          endMargin: $r('app.float.wh_value_8')
                        })
                        .scrollBar(BarState.Off)
                        .padding({
                          left: $r('app.float.wh_value_4'),
                          right: $r('app.float.wh_value_4'),
                          top: $r('app.float.wh_value_4'),
                          bottom: $r('app.float.wh_value_4')
                        })
                        .visibility(this.mShowUserCaPresenter.certList.length > 0
                          ? Visibility.Visible : Visibility.None)
                      }
                      .position({ y: $r('app.float.wh_value_0') })
                      .width(WidthPercent.WH_100_100)
                      .height(this.isStartBySheet ? WidthPercent.WH_AUTO : WidthPercent.WH_100_100)
                      .align(Alignment.Top)
                      .edgeEffect(EdgeEffect.Spring)
                      .scrollable(ScrollDirection.Vertical)
                      .scrollBar(BarState.Off)
                      .padding({
                        left: $r('app.float.wh_value_16'),
                        right: $r('app.float.wh_value_16'),
                        bottom: this.isStartBySheet ? $r('app.float.wh_value_80') : $r('app.float.wh_value_24')
                      })
                      .constraintSize({
                        minHeight: this.getScrollMinHeight()
                      }).onAreaChange((oldArea, newArea) => {
                        this.userScrollerHeight = newArea.height as number;
                      })

                      Column() {
                        ScrollBar({
                          scroller: this.userCaScroller,
                          direction: ScrollBarDirection.Vertical,
                          state: BarState.Auto
                        }).margin({
                          bottom: this.isStartBySheet ? $r('app.float.wh_value_80') : $r('app.float.wh_value_24')
                        })
                      }.height(this.userScrollerHeight)
                    }
                  }
                  .tabBar(this.TabBuilder(1))
                }
                .vertical(false)
                .scrollable(true)
                .barMode(BarMode.Fixed)
                .barWidth($r('app.float.tabs_barWidth_value'))
                .barHeight($r('app.float.tabs_barHeight_value'))
                .animationDuration(this.animationDurationNum)
                .width(WidthPercent.WH_100_100)
                .height(this.isStartBySheet ? WidthPercent.WH_AUTO : WidthPercent.WH_100_100)
                .onChange((index: number) => {
                  this.currentIndex = index;
                })
              }
              .height(this.isStartBySheet ? WidthPercent.WH_AUTO : WidthPercent.WH_100_100)
              .width(WidthPercent.WH_100_100)
              .padding({
                top: this.headRectHeight
              })
            }
            .width(WidthPercent.WH_100_100)
            .height(this.isStartBySheet ? WidthPercent.WH_AUTO : WidthPercent.WH_100_100)
          }
          .width(WidthPercent.WH_100_100)
          .height(this.isStartBySheet ? WidthPercent.WH_AUTO : WidthPercent.WH_100_100);
        }
      }
      .backgroundColor($r('sys.color.ohos_id_color_sub_background'))
      .width(WidthPercent.WH_100_100)
      .height(this.isStartBySheet ? WidthPercent.WH_AUTO : WidthPercent.WH_100_100);
    }
  }

  getScrollMinHeight() {
    if (this.sheetParam === undefined || this.headRectHeightReal === 0 ||
      this.sheetParam.sheetMinHeight < this.headRectHeightReal) {
      return 0;
    }
    return this.sheetParam.sheetMinHeight - this.headRectHeightReal - 56;
  }
}
```

### Patch
```diff
// File: CertManager/src/main/ets/pages/trustedCa.ets
--- a/CertManager/src/main/ets/pages/trustedCa.ets
+++ b/CertManager/src/main/ets/pages/trustedCa.ets
@@ -799,7 +799,7 @@
   isStartBySheetFirst: boolean = false;
   isStartBySheet: boolean = false;
   selected?: (path: string, param?: Object) => void;
-  @Prop sheetParam: SheetParam;
+  @ObjectLink sheetParam: SheetParam;
   @State headRectHeight: number = 64;
   @State headRectHeightReal: number = 0;
   @State private sysScrollerHeight: number = 0;


```

## [17/50] ID: OH_0016 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
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
@@ -215,7 +215,7 @@
               }
             }
           }
-        }, (item) => item.calllog.id.toString())
+        }, (item) => item.calllog.id.toString(), { cachedCount: 5 })
       }
       .width('100%')
       .listDirection(Axis.Vertical)
@@ -271,7 +271,7 @@
               }
             }
           }
-        }, (item) => item.contact.contactId.toString())
+        }, (item) => item.contact.contactId.toString(), { cachedCount: 5 })
       }
       .width('100%')
       .listDirection(Axis.Vertical)


```

## [18/50] ID: OH_0014 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
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
@@ -58,6 +58,7 @@
         .height($r("app.float.id_item_height_max"))
       }, item => item.id)
     }
+    .cachedCount(5)
     .divider({
       strokeWidth: 1,
       color: $r('sys.color.ohos_id_color_list_separator'),


```

## [19/50] ID: OH_0042 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/favorites/editFavoriteList.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
```typescript
@Component
struct FavoriteContent {
  @Link presenter: EditFavoriteListPresenter;
  isUsuallyShow: boolean = false;
  @Link selectNumbers: number;
  @Link favoriteNumber: number;
  @Link usuallyNumber: number;
  @State selectNumber: number = this.selectNumbers;
  @State selectFavoriteIdList: string[] = [];
  @State isEditSelectList: string[] = null != this.presenter.isEditSelect &&
    this.presenter.isEditSelect.length > 0 ? this.presenter.isEditSelect : [];
  @State favoriteListPresenter: EditFavoriteListPresenter = this.presenter;
  @State isSelectAll: boolean = false;
  @State isSelectAllStatus: boolean = false;
  item: FavoriteListBean = new FavoriteListBean(0,false,false,new FavoriteBean('',0,'','','','','',false,'',false,0,''),
    new SearchContactsBean('','','','','','','','','',0,'','','','','',''));
  @State text: string = '';
  @State isEditDrag: boolean = false;
  @State select: number = 0;
  @State currentIndex: number = 0;
  @State isDragShow: boolean = false;
  @State offsetY: number = 50;
  @State positionYDown: number = 0;
  @State positionYUp: number = 0;

  @Builder pixelMapBuilder() {
    Column() {
      FavoriteListItem({
        item: this.item,
        isEditSelectList: $isEditSelectList,
        presenter: $favoriteListPresenter,
        selectNumber: $selectNumber,
        isSelectAll: $isSelectAll,
        usuallyNumber: $usuallyNumber,
        favoriteNumber: $favoriteNumber,
        isEditDrag: this.isEditDrag
      })
    }
  }

  build() {
    Stack({ alignContent: Alignment.BottomEnd }) {
      Column() {
        Stack({ alignContent: Alignment.TopStart }) {
          Row() {
            Text(this.selectNumber > 0 ? $r('app.string.select_num', this.selectNumber) : $r('app.string.no_select'))
              .maxFontSize(22)
              .minFontSize(18)
              .maxLines(1)
              .fontWeight(FontWeight.Bold)
              .fontColor(Color.Black)
              .margin({ top: $r('app.float.id_card_margin_large'), bottom: $r('app.float.id_card_margin_large') })
          }
          .margin({ left: this.offsetY < 0 ? 0 : $r('app.float.id_item_height_mid') })
          .height(this.offsetY > 0 ? 56 : 138)
          .animation({
            duration: 200,
            iterations: 1,
          })

          TitleGuide({
            isDragShow: $isDragShow,
            isEditSelectList: $isEditSelectList,
            presenter: $favoriteListPresenter,
            selectNumber: $selectNumber,
            offsetY: $offsetY
          })
        }

        GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
          GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 1, lg: 2 } }) {
            List({ space: 0, initialIndex: 0 }) {
              LazyForEach(this.presenter.favoriteDataSource, (item: FavoriteListBean, index: number) => {
                ListItem() {
                  FavoriteListItem({
                    item: item,
                    isEditSelectList: $isEditSelectList,
                    presenter: $favoriteListPresenter,
                    selectNumber: $selectNumber,
                    isSelectAll: $isSelectAll,
                    usuallyNumber: $usuallyNumber,
                    favoriteNumber: $favoriteNumber,
                    isEditDrag: false
                  })
                }
                .onDragStart((event: DragEvent, extraParams: string) => {
                  console.log('ListItem onDragStarts, ' + extraParams)
                  let jsonString: Extra = JSON.parse(extraParams)
                  if (jsonString.selectedIndex >= this.favoriteNumber) {
                    console.log('List onDragStarts , return ')
                    return;
                  }
                  this.isEditDrag = true;
                  this.select = jsonString.selectedIndex;
                  this.item = item;
                  return this.pixelMapBuilder();
                })
              }, (item:FavoriteListBean) => JSON.stringify(item))
            }
            .editMode(true)
            .width('100%')
            .height('100%')
            .scrollBar(BarState.Off)
            .listDirection(Axis.Vertical)
            .edgeEffect(EdgeEffect.Spring)
            .onDrop((event: DragEvent, extraParams: string) => {
              let jsonString = JSON.parse(extraParams) as extraParamsObj;
              if (jsonString.insertIndex >= this.favoriteNumber) {
                return;
              }
              if (this.isEditDrag) {
                this.isDragShow = true;
                let index = this.presenter.favoriteDataSource.getFavoriteList().indexOf(this.item.favorite);
                this.presenter.favoriteDataSource.getFavoriteList().splice(index, 1);
                this.presenter.favoriteDataSource.getFavoriteList()
                  .splice(jsonString.insertIndex, 0, this.item.favorite);
                this.presenter.favoriteDataSource.refresh(this.presenter.favoriteDataSource.getFavoriteList());
                this.isEditDrag = false;
              }
            })
            .onScroll((scrollOffset, scrollState) => {
              this.offsetY = this.positionYDown - this.positionYUp;
              if (this.offsetY > 0) {
                animateTo({ duration: 1000 }, () => {
                });
              } else {
                animateTo({ duration: 1000 }, () => {
                });
              }
            })
            .onTouch((event) => {
              switch (event.type) {
                case TouchType.Down:
                  this.positionYDown = Math.abs(event.touches[0].y);
                  break;
                case TouchType.Move:
                  this.positionYUp = Math.abs(event.touches[0].y);
                case TouchType.Up:
                  this.positionYUp = Math.abs(event.touches[0].y);
                  break;
              }
            })
          }
        }
        .height('100%')
        .flexShrink(1)

        Row() {
          Flex({ direction: FlexDirection.Row, justifyContent: FlexAlign.SpaceBetween }) {
            Column() {
              Image(this.selectNumber > 0 ? $r('app.media.ic_public_close') : $r('app.media.ic_public_close_gray'))
                .objectFit(ImageFit.Contain)
                .height($r('app.float.id_card_image_small'))
                .width($r('app.float.id_card_image_small'))
                .margin({ bottom: 3 })
              Text($r('app.string.favorite_remove'))
                .fontColor(this.selectNumber > 0 ? $r('sys.color.ohos_id_color_toolbar_text') : Color.Gray)
                .fontSize($r('sys.float.ohos_id_text_size_caption'))
                .fontWeight(FontWeight.Medium)
                .margin({ top: $r('app.float.id_card_margin_large') })
            }
            .onClick(() => {
              if (this.isEditSelectList.length > 0) {
                this.presenter.deleteFavoriteInfo(this.isEditSelectList);
                this.isEditSelectList = [];
                this.selectNumber = this.isEditSelectList.length;
                router.back();
              }
            })
            .width('40%')
            .height('100%')
            .alignItems(HorizontalAlign.Center)
            .justifyContent(FlexAlign.Center)

            Column() {
              Image(this.presenter.favoriteList.length === this.selectNumber ? $r('app.media.ic_public_select_all_filled') : $r('app.media.ic_public_select_all'))
                .objectFit(ImageFit.Contain)
                .height($r('app.float.id_card_image_small'))
                .width($r('app.float.id_card_image_small'))
                .margin({ bottom: 3 })
                .fillColor($r('sys.color.ohos_id_color_primary'))
              Text(this.presenter.favoriteList.length === this.selectNumber ? $r('app.string.unselect_all') : $r('app.string.select_all'))
                .fontColor(this.presenter.favoriteList.length === this.selectNumber ? $r('sys.color.ohos_id_color_toolbar_text') : Color.Gray)
                .fontSize($r('sys.float.ohos_id_text_size_caption'))
                .fontWeight(FontWeight.Medium)
                .margin({ top: $r('app.float.id_card_margin_large') })

            }
            .onClick(() => {
              this.isSelectAll = this.presenter.favoriteList.length === this.selectNumber;
              if (this.isSelectAll) {
                this.isEditSelectList = this.presenter.cancelAllFavoriteSelectInfo(this.presenter.favoriteList, this.isEditSelectList);
              } else {
                this.isEditSelectList = this.presenter.addAllFavoriteSelectInfo(this.presenter.favoriteList);
              }
              this.selectNumber = this.isEditSelectList.length;
              this.presenter.favoriteDataSource.refresh(this.presenter.favoriteList);
            })
            .width('40%')
            .height('100%')
            .alignItems(HorizontalAlign.Center)
            .justifyContent(FlexAlign.Center)
          }
        }
        .padding({ left: 24, right: 24 })
        .backgroundColor(Color.White)
        .width('100%')
        .height($r('app.float.id_item_height_max'))
      }
      .padding({ left: 24, right: 24 })
      .height('100%')
      .width('100%')
    }
    .height('100%')
    .width('100%')
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/favorites/editFavoriteList.ets
--- a/entry/src/main/ets/pages/favorites/editFavoriteList.ets
+++ b/entry/src/main/ets/pages/favorites/editFavoriteList.ets
@@ -193,7 +193,7 @@
                   this.item = item;
                   return this.pixelMapBuilder();
                 })
-              }, (item:FavoriteListBean) => JSON.stringify(item))
+              }, (item:FavoriteListBean) => JSON.stringify(item), { cachedCount: 5 })
             }
             .editMode(true)
             .width('100%')


```

## [20/50] ID: OH_0089 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/hicar/HiCarContactSearchPage.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
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
@@ -274,7 +274,7 @@
           .width('100%')
         }
         .id(`HiCarContactSearch_SearchResultClick_ListItem_${index}`)
-      }, (item: LooseObject) => JSON.stringify(item))
+      }, (item: LooseObject) => JSON.stringify(item), { cachedCount: 5 })
     }
     .scrollBar(BarState.Off)
   }


```

## [21/50] ID: OH_0100 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSelectMemSendMsg.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
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
@@ -438,7 +438,7 @@
                 })
               }
               .width('100%')
-            }, (item: BatchSelectContact) => JSON.stringify(item))
+            }, (item: BatchSelectContact) => JSON.stringify(item), { cachedCount: 5 })
         }
 
         .width('100%')


```

## [22/50] ID: OH_0219 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-suggest-use-effectkit-blur`
- **Result:** `PASS`
- **Target File:** `product/phone/src/main/ets/pages/preview/PreviewBlurAnimationComponent.ets`
- **Warning:** Suggestion Use effectKit.createEffect to create a blur effect

###  Buggy Snippet
```typescript
Image(this.mScreenshotPixelMap)
          .width(this.pixelMapHorizontal ? this.getImgWidth() : this.getImgHeight())
          .height(this.pixelMapHorizontal ? this.getImgHeight() : this.getImgWidth())
          .rotate({
            angle: this.mScreenshotPixelMapAngle
          })
          .blur(this.mModeSwitchImgBlur)
```

### Patch
```diff
// File: product/phone/src/main/ets/pages/preview/PreviewBlurAnimationComponent.ets
--- a/product/phone/src/main/ets/pages/preview/PreviewBlurAnimationComponent.ets
+++ b/product/phone/src/main/ets/pages/preview/PreviewBlurAnimationComponent.ets
@@ -40,6 +40,7 @@
 import lazy { CommonConstants } from '@ohos/common/src/main/ets/statistics/CommonConstants';
 import lazy { PreviewAction } from '@ohos/common/src/main/ets/redux/actions/PreviewAction';
 import { ComponentSnapshotService } from '@ohos/common/src/main/ets/service/componentSnapshot/ComponentSnapshotService';
+import lazy { effectKit } from '@kit.ArkGraphics2D';
 
 const TAG: string = 'PreviewBlurAnimationComponent';
 
@@ -110,10 +111,11 @@
     y: BlurAnimateUtil.ROTATE_AXIS,
     angle: BlurAnimateUtil.IMG_FLIP_ANGLE_180
   }
-  @State mModeSwitchImgBlur: number = 0;
+  @State @Watch('onBlurRadiusChange') mModeSwitchImgBlur: number = 0;
   @State mModeSwitchImgOpacity: number = 1;
   @State visibleAreaWidth: number = 0;
   @State visibleAreaHeight: number = 0;
+  @State blurredPixelMap: image.PixelMap | null = null;
   @StorageLink('isLemCollaps') isLemCollaps: boolean = false;
   @StorageLink('isInBlurAnim') isInBlurAnim: boolean = false;
   @StorageLink('isShowPhotoBrowser') @Watch('changeImgBlurValue') isShowPhotoBrowser: boolean = false;
@@ -330,6 +332,10 @@
   private pixelMapAngleChange(): void {
     this.pixelMapHorizontal = this.mScreenshotPixelMapAngle === 0 || this.mScreenshotPixelMapAngle === 180;
     HiLog.d(TAG, `pixelMapHorizontal: ${this.pixelMapHorizontal}`);
+  }
+
+  private onBlurRadiusChange(): void {
+    this.applyBlurWithEffectKit(this.mScreenshotPixelMap, this.mModeSwitchImgBlur);
   }
 
   private async prepareBlurImage(): Promise<void> {
@@ -517,6 +523,7 @@
       HiLog.i(TAG, 'release pixelMap after disappear')
       this.mScreenshotPixelMap?.release();
       this.staticBlur?.release();
+      this.blurredPixelMap?.release();
     }
   }
 
@@ -564,6 +571,7 @@
         this.isLemModeSwitched = true;
         this.mScreenshotPixelMap?.release();
         this.staticBlur?.release();
+        this.blurredPixelMap?.release();
       }
     }, () => {
       this.mModeSwitchImgOpacity = 0;
@@ -763,6 +771,25 @@
     return scale;
   }
 
+  private async applyBlurWithEffectKit(pixelMap: image.PixelMap | null, blurRadius: number): Promise<void> {
+    if (!pixelMap || blurRadius === 0) {
+      this.blurredPixelMap = pixelMap;
+      return;
+    }
+    try {
+      const effect = effectKit.createEffect(pixelMap);
+      if (effect) {
+        effect.blur(blurRadius);
+        this.blurredPixelMap = await effect.getPixelMap();
+      } else {
+        this.blurredPixelMap = pixelMap;
+      }
+    } catch (error) {
+      HiLog.e(TAG, `applyBlurWithEffectKit error: ${JSON.stringify(error)}`);
+      this.blurredPixelMap = pixelMap;
+    }
+  }
+
   @Builder
   BlurredPixelMapBuilder(): void {
     Stack() {
@@ -773,13 +800,12 @@
           .syncLoad(true)
           .draggable(false)
       } else {
-        Image(this.mScreenshotPixelMap)
+        Image(this.blurredPixelMap ?? this.mScreenshotPixelMap)
           .width(this.pixelMapHorizontal ? this.getImgWidth() : this.getImgHeight())
           .height(this.pixelMapHorizontal ? this.getImgHeight() : this.getImgWidth())
           .rotate({
             angle: this.mScreenshotPixelMapAngle
           })
-          .blur(this.mModeSwitchImgBlur)
           .syncLoad(true)
           .draggable(false)
           .autoResize(true)


```

## [23/50] ID: OH_0260 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-object-link-to-replace-prop`
- **Result:** `PASS`
- **Target File:** `product/phone/src/main/ets/pages/biometricsandpassword/component/MenuComponent.ets`
- **Warning:** Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

###  Buggy Snippet
```typescript
@Component
struct MultiLargeEntryComponent {
  @Prop menu: MenuEntry;
  index: number = -1;

  @Styles
  normalStyles() {
    .backgroundColor(Color.Transparent)
    .borderRadius($r('sys.float.ohos_id_corner_radius_card'))
  }

  @Styles
  pressedStyles() {
    .backgroundColor($r('sys.color.ohos_id_color_click_effect'))
    .borderRadius($r('sys.float.ohos_id_corner_radius_card'))
  }

  build() {
    Column() {
      Column() {
        Column() {
          Text(this.menu?.title)
            .fontColor(this.menu?.style?.fontColor ? this.menu.style.fontColor : $r('sys.color.ohos_id_color_text_primary'))
            .fontSize(this.menu?.style?.fontSize ? this.menu.style.fontSize : $r('sys.float.ohos_id_text_size_body1'))
            .fontWeight(this.menu?.style?.fontWeight ? this.menu.style.fontWeight : FontWeight.Medium)
            .textAlign(TextAlign.Start)
            .wordBreak(WordBreak.BREAK_WORD)
            .width('90%')
        }
        .width('100%')
        .padding({ top: FontScaleUtils.getCurrentPadding(),
          left: $r('app.float.padding_8'),
          right: $r('app.float.padding_8')
        })
        .alignItems(HorizontalAlign.Start);
        Row() {
          Text(this.menu?.subTitle)
            .fontColor($r('sys.color.ohos_id_color_text_secondary'))
            .fontSize($r('sys.float.ohos_id_text_size_sub_title3'))
            .width('90%')
            .textAlign(TextAlign.Start)
          Image($r('app.media.ic_settings_arrow'))
            .size({
              width: '12vp',
              height: '24vp',
            })
            .margin({
              start: PADDING_8,
              top: PADDING_0,
              bottom: PADDING_0,
            })
            .draggable(false)
            .matchTextDirection(true);
        }
        .padding({
          bottom: FontScaleUtils.getCurrentPadding(),
          left: $r('app.float.padding_8'),
          right: $r('app.float.padding_8'),
        })
        .justifyContent(FlexAlign.SpaceBetween)
        .alignItems(VerticalAlign.Center)
        .width('100%')
      }
      .hoverEffect(HoverEffect.Highlight)
      .stateStyles({
        normal: this.normalStyles,
        pressed: this.pressedStyles,
      })
      .onClick(() => {
        if (this.menu?.onMenuClick) {
          this.menu?.onMenuClick(this.index);
        }
      })
      .focusBox({
        margin: FOCUS_BOX_PADDING_METRICS
      })
    }
    .margin({
      left: $r('app.float.padding_4'),
      right: $r('app.float.padding_4'),
    })
  }
}
```

### Patch
```diff
// File: product/phone/src/main/ets/pages/biometricsandpassword/component/MenuComponent.ets
--- a/product/phone/src/main/ets/pages/biometricsandpassword/component/MenuComponent.ets
+++ b/product/phone/src/main/ets/pages/biometricsandpassword/component/MenuComponent.ets
@@ -424,7 +424,7 @@
 
 @Component
 struct EntryComponent {
-  @Prop menu: MenuEntry;
+  @ObjectLink menu: MenuEntry;
   index: number = -1;
 
   @Styles
@@ -495,7 +495,7 @@
 
 @Component
 struct MultiLargeEntryComponent {
-  @Prop menu: MenuEntry;
+  @ObjectLink menu: MenuEntry;
   index: number = -1;
 
   @Styles
@@ -579,7 +579,7 @@
 
 @Component
 struct MultiEntryComponent {
-  @Prop menu: MenuEntry;
+  @ObjectLink menu: MenuEntry;
   index: number = -1;
 
   @Styles
@@ -669,7 +669,7 @@
 
 @Component
 struct FgIdTextComponent {
-  @Prop menu?: MenuEntry;
+  @ObjectLink menu: MenuEntry;
   index: number = -1;
   clickModifier: ClickModifier = new ClickModifier(this.index, this.menu?.onMenuClick);
 
@@ -720,7 +720,7 @@
 
 @Component
 struct FgUnderIdTextComponent {
-  @Prop menu?: MenuEntry;
+  @ObjectLink menu: MenuEntry;
   index: number = -1;
   clickModifier: ClickModifier = new ClickModifier(this.index, this.menu?.onMenuClick);
 


```

## [24/50] ID: OH_0378 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-reusable-component`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/example/thirdpartyscenes/Scene_4.ets`
- **Warning:** Use reusable components to define complex components whenever possible

###  Buggy Snippet
```typescript
@Component
struct Scene_4 {
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
  private data: MyDataSource = new MyDataSource();

  async aboutToAppear() {
    try {
      for (let i = 0; i < this.animationPaths.length; i++) {
        this.data.pushData(this.animationPaths[i])
      }
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
          LazyForEach(this.data, (path: string, index) => {
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
        }.cachedCount(5)
        .height('100%')
        .width('100%')
      }
    }
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/example/thirdpartyscenes/Scene_4.ets
--- a/entry/src/main/ets/pages/example/thirdpartyscenes/Scene_4.ets
+++ b/entry/src/main/ets/pages/example/thirdpartyscenes/Scene_4.ets
@@ -15,6 +15,54 @@
 
 import { LottieView, LottieController, lottie } from '@ohos/lottie-turbo'
 import common from '@ohos.app.ability.common'
+
+@Reusable
+@Component
+struct AnimationListItem {
+  path: string = ''
+  controller: LottieController = new LottieController()
+  @State fileName: string = ''
+
+  aboutToAppear() {
+    this.fileName = this.getFileName(this.path)
+  }
+
+  aboutToReuse(params: Record<string, Object>) {
+    this.path = params.path as string
+    this.controller = params.controller as LottieController
+    this.fileName = this.getFileName(this.path)
+  }
+
+  getFileName(path: string): string {
+    return path.split('/').pop()?.replace('.json', '') || ''
+  }
+
+  build() {
+    Column() {
+      LottieView({
+        loop: true,
+        autoplay: true,
+        autoSkip: true,
+        path: $rawfile(this.path),
+        controller: this.controller,
+      })
+        .width('60%')
+        .height('30%')
+        .aspectRatio(1)
+        .backgroundColor('#F1F3F5')
+        .margin(10)
+        .onClick(() => {
+          this.controller.play()
+        })
+      Text(this.fileName)
+        .fontSize(14)
+        .margin({ top: 5, bottom: 5 })
+        .textAlign(TextAlign.Center)
+        .maxLines(2)
+        .textOverflow({ overflow: TextOverflow.Ellipsis })
+    }
+  }
+}
 
 @Entry
 @Component
@@ -63,10 +111,6 @@
     .justifyContent(FlexAlign.Center)
   }
 
-  getFileName(path: string): string {
-    return path.split('/').pop()?.replace('.json', '') || ''
-  }
-
   build() {
     Column() {
       if (this.isLoading) {
@@ -75,29 +119,7 @@
         List({ space: 5, initialIndex: 4, scroller: this.scroller }) {
           LazyForEach(this.data, (path: string, index) => {
             ListItem() {
-              Column() {
-                LottieView({
-                  loop: true,
-                  autoplay: true,
-                  autoSkip: true,
-                  path: $rawfile(path),
-                  controller: this.controllers[index],
-                })
-                  .width('60%')
-                  .height('30%')
-                  .aspectRatio(1)
-                  .backgroundColor('#F1F3F5')
-                  .margin(10)
-                  .onClick(() => {
-                    this.controllers[index].play()
-                  })
-                Text(this.getFileName(path))
-                  .fontSize(14)
-                  .margin({ top: 5, bottom: 5 })
-                  .textAlign(TextAlign.Center)
-                  .maxLines(2)
-                  .textOverflow({ overflow: TextOverflow.Ellipsis })
-              }
+              AnimationListItem({ path: path, controller: this.controllers[index] })
             }
           })
         }.cachedCount(5)


```

## [25/50] ID: OH_0244 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/transmitmsg/transmitSearchMsgPage.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
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
@@ -266,7 +266,7 @@
           ListItem() {
             this.searchItem(item, index)
           }
-        }, (item: MyItem) => JSON.stringify(item));
+        }, (item: MyItem, index: number) => `${item.index}_${index}`);
 
       if (this.transmitSearchMsgCtrl.searchList.length > 3) {
         this.listItemCollapseOpen()
@@ -582,7 +582,7 @@
           }
           .width('100%')
           .height(this.fontSizeScale >= 1.45 ? (this.fontSizeScale * 60) + 'vp' : (this.fontSizeScale * 80) + 'vp')
-        }, (item: messageType) => JSON.stringify(item))
+        }, (item: messageType) => item.threadId?.toString() || '')
       }
       .divider({
         strokeWidth: $r('app.float.settings_divider_strokeWidth'),


```

## [26/50] ID: OH_0081 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/group/GroupList.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
```typescript
@Component
struct GroupContent {
  @Link presenter: GroupListPresenter;
  @Link intelligenceGroupPresenter: IntelligenceGroupListPresenter;
  @State intelligenceGroupNameList: string[] = ['origanization', 'city', 'latestcontact'];
  @State mPresenter: GroupListPresenter = this.presenter;
  @State otherIntelligenceGroupPresenter: IntelligenceGroupListPresenter = this.intelligenceGroupPresenter;
  @Link aPresenter: ArrangeContactsPresenter;
  groupAccountName: String | undefined = AppStorage.Get('groupAccountName')
  @StorageLink('breakpoint') curBp: string = 'sm';
  @StorageLink('spaceLR') spaceLR: Resource = $r('sys.float.padding_level8');
  @StorageProp('isTabletLandscape') isTabletLandscape: boolean = false;
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;
  @StorageProp('splitStatus') splitStatus: SplitStatus = SplitStatus.DEFAULT;
  private isPC: boolean = EnvironmentProp.isPC();
  editDialog: CustomDialogController | null = null;
  newGroupAccountDialog: CustomDialogController | null = null;
  // 是否显示在VisionGlass
  @StorageProp(VisionGlassConstants.KEY_IS_IN_VISION_GLASS) isInVisionGlass: boolean = false;
  private scroller: Scroller = new Scroller();

  build() {

    Stack({ alignContent: Alignment.BottomEnd }) {

      Column() {

        GridRow({ 
          columns: { sm: 4, md: 8, lg: 12 },
          gutter: { x: 12, y: 0 }
        }) {

          GridCol({ span: { sm: 4, md: 8, lg: 12 } }) {

            List({ scroller: this.scroller }) {

              if (this.isPC) {
                // PC端子标题
                PCSubTitle({ subtitle: $r('app.string.intelligence_group') })
              } else {
                // 智能群组标题
                SubHeader({
                  secondaryTitle: $r('app.string.intelligence_group'),
                  secondaryTitleModifier: this.isThemeActive ?
                  new TextModifier().fontColor($r('app.color.skin_font_secondary')) : undefined
                })
                  .margin({ left: this.curBp === 'lg' ? '8vp' : 0 })
              }


              ListItemGroup({ style: ListItemGroupStyle.CARD }) {

                ForEach(this.intelligenceGroupNameList, (item: string, index: number) => {
                  ListItem() {
                    // 弹性布局
                    Flex({
                      direction: FlexDirection.Column,
                      justifyContent: FlexAlign.Center,
                      alignItems: ItemAlign.Start
                    }) {
                      // 智能群组列表项组件
                      IntelligenceGroupListItem({
                        item: item, // 智能群组名称
                        type: index, // 智能群组类型索引
                        intelligenceGroupPresenter: $intelligenceGroupPresenter // 智能群组列表presenter引用
                      })
                        .id('IntelligenceGrouoList_Contacts_LongPressGesture_GroupListItem')
                    }
                    .backgroundColor(Color.Transparent)
                    .width('100%')
                  }
                  .backgroundColor(Color.Transparent)
                })
              }

              .borderRadius(this.isPC ? '16vp' : $r('sys.float.corner_radius_level10'))
              .margin({
                left: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_left'),
                right: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_right')
              })
              .backgroundColor(this.isPC ? $r('sys.color.comp_background_list_card') :
              $r('app.color.skin_comp_background_list_card'))
              .divider({
                strokeWidth: '1px',
                startMargin: '8vp',
                endMargin: '8vp',
                color: $r('app.color.skin_ohos_id_color_list_separator'),
              })
              .width('100%')


              if (this.presenter.groupCount > 0) {
                ForEach(this.aPresenter.accountList, (item1: AccountVo, index?: number) => {
                  if (this.isPC) {
                    PCSubTitle({ subtitle: $r('app.string.computer') })
                  } else {
                    SubHeader({
                      secondaryTitle: (this.curBp === 'lg' && !this.isInVisionGlass) ? $r('app.string.tablet') :
                      $r('app.string.telep_group'),
                      secondaryTitleModifier: this.isThemeActive ?
                      new TextModifier().fontColor($r('app.color.skin_font_secondary')) : undefined
                    })
                      .margin({ left: this.curBp === 'lg' ? '8vp' : 0 })
                  }

                  ListItemGroup({ style: ListItemGroupStyle.CARD }) {
                    LazyForEach(this.presenter.groupListDataSource, (item: GroupInfo) => {
                      ListItem() {
                        Flex({
                          direction: FlexDirection.Column,
                          justifyContent: FlexAlign.Center,
                          alignItems: ItemAlign.Start
                        }) {
                          if (item1.accountId == item.group.accountId) {
                            GroupListItem({ item: item, mPresenter: $mPresenter })
                              .id('GrouoList_Contacts_LongPressGesture_GroupListItem')
                          }
                        }
                        .backgroundColor(Color.Transparent)
                        .width('100%')
                      }
                      .backgroundColor(Color.Transparent)
                    }, (item: GroupInfo) => JSON.stringify(item))
                  }
                  .borderRadius(this.isPC ? '16vp' : $r('sys.float.corner_radius_level10'))
                   .margin({
                    left: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_left'),
                    right: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_right'),
                    bottom: $r('app.float.id_card_margin_xxl')
	                })
                  .backgroundColor(this.isPC ? $r('sys.color.comp_background_list_card') :
                  $r('app.color.skin_comp_background_list_card'))
                  .divider({
                    strokeWidth: '1px',
                    startMargin: '8vp',
                    endMargin: '8vp',
                    color: $r('app.color.skin_ohos_id_color_list_separator'),
                  })
                  .width('100%')
                })
              }
            }
            .scrollBar(BarState.Off)
            .editMode(true)
            .width('100%')
            .height('100%')
            .listDirection(Axis.Vertical)
            .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
            .clipContent(ContentClipMode.SAFE_AREA)
            // .safeAreaPadding({ top: this.isPC ? 0 : $r('app.float.id_hds_title_margin') })
          }
        }
        .height('100%')
        .flexShrink(1)

        GridRow({ columns: { sm: 4, md: 8, lg: 8 }, gutter: { x: 12, y: 0 } }) {
          GridCol({ span: { sm: 4, md: 8, lg: 6 }, offset: { sm: 0, md: 0, lg: 1 } }) {
            if (!this.isPC) {
              bottomContent({
                presenter: $mPresenter,
                aPresenter: $aPresenter,
                editDialog: this.editDialog,
                newGroupAccountDialog: this.newGroupAccountDialog
              })
            }
          }
        }
        .margin({
          top: this.isPC ? 0 : '2vp',
          left: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_left'),
          right: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_right')
        })
      }
      .padding({

        bottom: this.splitStatus === SplitStatus.VERTICAL_SPLIT || !this.isPC ?
          $r('app.float.id_item_height_large'):0
      })
      .height('100%')
      .width('100%')
    }
    .backgroundColor(this.isThemeActive ? undefined : $r('app.color.color_bind_sheet_background'))
    .height('100%')
    .width('100%')
  }

  // 分组列表
  @Builder
  groupListBuilder(item1: AccountVo, item: GroupInfo) {
    Flex({
      direction: FlexDirection.Column,
      justifyContent: FlexAlign.Center,
      alignItems: ItemAlign.Start
    }) {
      if (item1.accountId == item.group.accountId) {
        GroupListItem({ item: item, mPresenter: $mPresenter })
          .id('GrouoList_Contacts_LongPressGesture_GroupListItem');
      }
    }
    .width('100%')
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/group/GroupList.ets
--- a/entry/src/main/ets/pages/group/GroupList.ets
+++ b/entry/src/main/ets/pages/group/GroupList.ets
@@ -675,14 +675,14 @@
                         .width('100%')
                       }
                       .backgroundColor(Color.Transparent)
-                    }, (item: GroupInfo) => JSON.stringify(item))
+                    }, (item: GroupInfo) => JSON.stringify(item), { cachedCount: 5 })
                   }
                   .borderRadius(this.isPC ? '16vp' : $r('sys.float.corner_radius_level10'))
                    .margin({
                     left: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_left'),
                     right: (this.isPC || this.curBp === 'lg') ? '24vp' : $r('sys.float.margin_right'),
                     bottom: $r('app.float.id_card_margin_xxl')
-	                })
+                        })
                   .backgroundColor(this.isPC ? $r('sys.color.comp_background_list_card') :
                   $r('app.color.skin_comp_background_list_card'))
                   .divider({


```

## [27/50] ID: OH_0321 | ArkTS (T)
- **Rule ID:** `@hw-stylistic/quotes`
- **Result:** `PASS`
- **Target File:** `HMRouterLibrary/src/main/ets/router/HMLifecycleMgr.ets`
- **Warning:** Strings must use single quotes.

###  Buggy Snippet
```typescript
{
{
{
      let singletonPageKey: string = ''
      for (let value of this.lifecycleMap) {
        if (value[0].includes(pageUrl)) {
          singletonPageKey = value[0]
          break
        }
      }
      let currentLifecycle = this.lifecycleMap.get(singletonPageKey)
      if (currentLifecycle) {
        await currentLifecycle?.getLifecycle(pageUrl, onceLifecycle)
        return currentLifecycle
      } else {
        currentLifecycle = new HMLifecycleHandle()
        currentLifecycle.singleton = true
        this.lifecycleMap.set(pageUrl, currentLifecycle)
        HMLogger.d("[HMLifecycle] register lifecycle")
        await currentLifecycle.getLifecycle(pageUrl, onceLifecycle)
        HMLogger.d("[HMLifecycle] register lifecycle finished")
        return currentLifecycle
      }
    }
    let currentLifecycle = new HMLifecycleHandle()
    this.lifecycleMap.set(pageUrl, currentLifecycle)
    HMLogger.d("[HMLifecycle] register lifecycle")
    await currentLifecycle.getLifecycle(pageUrl, onceLifecycle)
    HMLogger.d("[HMLifecycle] register lifecycle finished")
    return currentLifecycle
  }

  destroyHMLifecycle(pageUrl: string, navId: string) {
    // 销毁生命周期实例
    let currentLifecycleHandle = this.lifecycleMap.get(pageUrl + navId)
    this.lifecycleMap.delete(pageUrl + navId)
    HMRouterStore.getInstance().releaseLifecycle(pageUrl, currentLifecycleHandle?.pageId!)
  }

  updateLifecycleNavContext(pageUrl: string, navContext: NavDestinationContext) {
    const currentLifecycleHandle = this.lifecycleMap.get(pageUrl)
    if (!currentLifecycleHandle) {
      HMLogger.e(HMError.ERR_INTERNAL, "[HMLifecycle] lifecycle registered error")
      return;
    }
    currentLifecycleHandle.navContext = navContext
    currentLifecycleHandle.navId = navContext.navDestinationId!
    currentLifecycleHandle.lifecycleContext = new HMLifecycleContext(this.uiContext!, navContext)
    if (!currentLifecycleHandle.singleton) {
      currentLifecycleHandle.pageId = Date.now().toString()
    }
    HMRouterStore.getInstance()
      .updateLifecycle(pageUrl, currentLifecycleHandle.pageId, '', navContext.navDestinationId!)
    this.lifecycleMap.set(pageUrl + navContext.navDestinationId!, currentLifecycleHandle)
    this.lifecycleMap.delete(pageUrl)
  }
}
```

### Patch
```diff
// File: HMRouterLibrary/src/main/ets/router/HMLifecycleMgr.ets
--- a/HMRouterLibrary/src/main/ets/router/HMLifecycleMgr.ets
+++ b/HMRouterLibrary/src/main/ets/router/HMLifecycleMgr.ets
@@ -47,17 +47,17 @@
         currentLifecycle = new HMLifecycleHandle()
         currentLifecycle.singleton = true
         this.lifecycleMap.set(pageUrl, currentLifecycle)
-        HMLogger.d("[HMLifecycle] register lifecycle")
+        HMLogger.d('[HMLifecycle] register lifecycle')
         await currentLifecycle.getLifecycle(pageUrl, onceLifecycle)
-        HMLogger.d("[HMLifecycle] register lifecycle finished")
+        HMLogger.d('[HMLifecycle] register lifecycle finished')
         return currentLifecycle
       }
     }
     let currentLifecycle = new HMLifecycleHandle()
     this.lifecycleMap.set(pageUrl, currentLifecycle)
-    HMLogger.d("[HMLifecycle] register lifecycle")
+    HMLogger.d('[HMLifecycle] register lifecycle')
     await currentLifecycle.getLifecycle(pageUrl, onceLifecycle)
-    HMLogger.d("[HMLifecycle] register lifecycle finished")
+    HMLogger.d('[HMLifecycle] register lifecycle finished')
     return currentLifecycle
   }
 
@@ -71,7 +71,7 @@
   updateLifecycleNavContext(pageUrl: string, navContext: NavDestinationContext) {
     const currentLifecycleHandle = this.lifecycleMap.get(pageUrl)
     if (!currentLifecycleHandle) {
-      HMLogger.e(HMError.ERR_INTERNAL, "[HMLifecycle] lifecycle registered error")
+      HMLogger.e(HMError.ERR_INTERNAL, '[HMLifecycle] lifecycle registered error')
       return;
     }
     currentLifecycleHandle.navContext = navContext


```

## [28/50] ID: OH_0288 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/LazyForEachApng.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
```typescript
@ComponentV2
struct LazyForEachApng {
  @Local speedRate: number = (router.getParams() as routerParams).speedRate;
  private scrollForList: Scroller = new Scroller();
  private data: SwiperDataSource =
    new SwiperDataSource([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
      26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50])

  build() {
    Column() {
      Row() {
        Button($r('app.string.back')).onClick(() => {
          router.back()
        })
      }

      Column() {
        Text($r('app.string.Load_multiple_APNG_images_by_LazyForEach'))
        List({ scroller: this.scrollForList }) {
          LazyForEach(this.data, (item: number) => {
            ListItem() {
              apngV2({
                src: $r('app.media.stack'),
                speedRate: this.speedRate!!,
                apngWidth: 100,
                apngHeight: 100
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
@@ -91,7 +91,7 @@
               })
             }
             .height(100).margin({ left: 10, right: 10, top: 10 })
-          }, (item: string) => item)
+          }, (item: string) => item, { cachedCount: 5 })
         }
         .width("100%")
         .height("100%")


```

## [29/50] ID: OH_0316 | ArkTS (T)
- **Rule ID:** `@hw-stylistic/no-tabs`
- **Result:** `PASS`
- **Target File:** `HMRouterLibrary/src/main/ets/router/AbstractLifecycle.ets`
- **Warning:** Unexpected tab character.

###  Buggy Snippet
```typescript
onAppear(ctx: HMLifecycleContext): HMLifecycleAction {
    return HMLifecycleAction.DO_NEXT()
  }

  onDisAppear(ctx: HMLifecycleContext): HMLifecycleAction {
    return this.runObserver(HMLifecycleState.onDisAppear, ctx)
  }

  onShown(ctx: HMLifecycleContext): HMLifecycleAction {
    return this.runObserver(HMLifecycleState.onShown, ctx)
  }

  onHidden(ctx: HMLifecycleContext): HMLifecycleAction {
    return this.runObserver(HMLifecycleState.onHidden, ctx)
  }

  onWillAppear(ctx: HMLifecycleContext): HMLifecycleAction {
    return HMLifecycleAction.DO_NEXT()
  }

  onWillDisappear(ctx: HMLifecycleContext): HMLifecycleAction {
    return this.runObserver(HMLifecycleState.onWillDisappear, ctx)
  }

  onWillShow(ctx: HMLifecycleContext): HMLifecycleAction {
		return HMLifecycleAction.DO_NEXT()
	}

  onWillHide(ctx: HMLifecycleContext): HMLifecycleAction {
    return this.runObserver(HMLifecycleState.onWillHide, ctx)
  }

  onReady(ctx: HMLifecycleContext): HMLifecycleAction {
    return HMLifecycleAction.DO_NEXT()
  }

  onBackPressed(ctx: HMLifecycleContext): HMLifecycleAction {
    return this.runObserver(HMLifecycleState.onBackPressed, ctx)
  }

  addObserver(state: HMLifecycleState, callback: (ctx: HMLifecycleContext) => HMLifecycleAction): void {
    let callbackArr: undefined | Array<(ctx: HMLifecycleContext) => HMLifecycleAction> =
      this.observerMap.get(state);
    if (callbackArr) {
      callbackArr.push(callback);
    } else {
      this.observerMap.set(state, [callback]);
    }
  }

  runObserver(state: HMLifecycleState, ctx: HMLifecycleContext): HMLifecycleAction {
    if (this.observerMap.has(state)) {
      let observerArray = this.observerMap.get(state)
      let action: HMLifecycleAction
      for (let i = 0; i < observerArray!.length; i++) {
}
}
}
```

### Patch
```diff
// File: HMRouterLibrary/src/main/ets/router/AbstractLifecycle.ets
--- a/HMRouterLibrary/src/main/ets/router/AbstractLifecycle.ets
+++ b/HMRouterLibrary/src/main/ets/router/AbstractLifecycle.ets
@@ -49,8 +49,8 @@
   }
 
   onWillShow(ctx: HMLifecycleContext): HMLifecycleAction {
-		return HMLifecycleAction.DO_NEXT()
-	}
+    return HMLifecycleAction.DO_NEXT()
+  }
 
   onWillHide(ctx: HMLifecycleContext): HMLifecycleAction {
     return this.runObserver(HMLifecycleState.onWillHide, ctx)


```

## [30/50] ID: OH_0365 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-state-var-access-in-loop`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/MainAbility/pages/OnePlusNLayoutSample.ets`
- **Warning:** Avoid frequent state variable reads inside loop logic

###  Buggy Snippet
```typescript
for (let i = 0;i < this.beArr.length; i++) {
            this.textCount += this.beArr[i]
          }
```

### Patch
```diff
// File: entry/src/main/ets/MainAbility/pages/OnePlusNLayoutSample.ets
--- a/entry/src/main/ets/MainAbility/pages/OnePlusNLayoutSample.ets
+++ b/entry/src/main/ets/MainAbility/pages/OnePlusNLayoutSample.ets
@@ -510,9 +510,12 @@
         }
         if (this.num == 0) {
           this.beArr = afArr
-          for (let i = 0;i < this.beArr.length; i++) {
-            this.textCount += this.beArr[i]
+          const beArrLocal = this.beArr
+          let count = 0
+          for (let i = 0;i < beArrLocal.length; i++) {
+            count += beArrLocal[i]
           }
+          this.textCount = count
         } else {
           this.compare(this.beArr, afArr)
           let after = 0


```

## [31/50] ID: OH_0162 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-object-link-to-replace-prop`
- **Result:** `PASS`
- **Target File:** `CertManager/src/main/ets/pages/picker/InstallPage.ets`
- **Warning:** Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

###  Buggy Snippet
```typescript
@Component
export struct InstallPage {
  private stack?: NavPathStack;

  @Prop sheetParam: SheetParam;

  build() {
    NavDestination() {
      Column() {
        CertInstallFromStorage({
          isStartBySheet: true,
          sheetParam: this.sheetParam,
          selected: (path, param) => {
            if (path === NavEntryKey.POP) {
              this.stack?.pop();
            } else {
              this.stack?.pushPath(new NavPathInfo(path, param));
            }
          }
        })
      }
    }
    .hideTitleBar(true)
    .width(WidthPercent.WH_100_100)
    .height(WidthPercent.WH_AUTO)
    .backgroundColor($r('sys.color.background_secondary'))
    .onReady((ctx: NavDestinationContext) => {
      this.stack = ctx.pathStack;
    })
  }
}
```

### Patch
```diff
// File: CertManager/src/main/ets/pages/picker/InstallPage.ets
--- a/CertManager/src/main/ets/pages/picker/InstallPage.ets
+++ b/CertManager/src/main/ets/pages/picker/InstallPage.ets
@@ -22,7 +22,7 @@
 export struct InstallPage {
   private stack?: NavPathStack;
 
-  @Prop sheetParam: SheetParam;
+  @ObjectLink sheetParam: SheetParam;
 
   build() {
     NavDestination() {


```

## [32/50] ID: OH_0091 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/hicar/HiCarContactSearchPage.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
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
@@ -274,7 +274,7 @@
           .width('100%')
         }
         .id(`HiCarContactSearch_SearchResultClick_ListItem_${index}`)
-      }, (item: LooseObject) => JSON.stringify(item))
+      }, (item: LooseObject) => item.contact.entityId.toString())
     }
     .scrollBar(BarState.Off)
   }


```

## [33/50] ID: OH_0200 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `HMSliderPlayer/src/main/ets/components/HMSliderPlayer.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
```typescript
@Component
export struct HMSliderPlayer {
  @State curIndex: number = 0;
  @State foldStatus: number = 0;
  @State sliderPlayerSize: SliderPlayerSize = new SliderPlayerSize();
  @State sliderPlayerDirection: SliderPlayerDirection = new SliderPlayerDirection();
  @Link hmSliderPlayerController: HMSliderPlayerController;
  private datasource: HMSliderPlayerIDataSource = new HMSliderPlayerIDataSource();
  private swiperController: SwiperController = new SwiperController();
  private hmAVPlayerMgr: HMAVPlayerMgr = new HMAVPlayerMgr();
  private options?: HMSliderPlayerOptions;
  private windowMgr: WindowMgr = WindowMgr.getInstance();

  aboutToAppear(): void {
    this.hmSliderPlayerController?.set(this.hmAVPlayerMgr);
    this.hmSliderPlayerController?.set(this.sliderPlayerSize);
    this.hmSliderPlayerController?.set(this.sliderPlayerDirection);
    WindowMgr.getInstance().setUIContext(this.getUIContext())
    window.getLastWindow(this.getUIContext().getHostContext(), (err: BusinessError, data) => {
      if (err.code) {
        Logger.error('Failed to obtain the top window. Code: %{public}d, message: %{public}s', err.code,
          err.message);
      }
      this.windowMgr.setWindowStage(data);
      this.windowMgr.registerOnWindowSizeChange((size: window.Size) => {

      })
    });
  }

  build() {
    Column() {
      Stack({ alignContent: Alignment.TopStart }) {
        Swiper(this.swiperController) {
          LazyForEach(this.datasource,
            (item: HMVideoSliderPlayerDataSource | HMCustomSliderPlayerDataSource, index: number) => {
              HMVideoSliderComponent({
                index: index,
                datasource: item,
                curIndex: this.curIndex,
                foldStatus: this.foldStatus,
                avPlayerCallback: this.options?.avPlayerCallback,
                hmAVPlayerMgr: this.hmAVPlayerMgr,
                hmSliderPlayerController: this.hmSliderPlayerController
              });
            }, (item: HMSliderPlayerDataSource, index: number) => JSON.stringify(item) + index);
        }
        .cachedCount(CommonConstant.DEFAULT_SWIPER_CACHE_COUNT)
        .width(CommonConstant.FULL_PERCENT_WIDTH)
        .height(CommonConstant.FULL_PERCENT_HEIGHT)
        .vertical(true)
        .loop(false)
        .curve(Curve.Ease)
        .duration(CommonConstant.DURATION_TIME)
        .indicator(false)
        .backgroundColor(Color.Black)
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
        .onGestureSwipe((index: number, extraInfo: SwiperAnimationEvent) => {
          if (this.options?.swiperCallback?.onGestureSwipe) {
            this.options.swiperCallback?.onGestureSwipe(index, extraInfo);
          }
        })
        .customContentTransition(this.options?.swiperCallback?.customContentTransition)
        .onContentDidScroll((selectedIndex: number, index: number, position: number, mainAxisLength: number) => {
          if (this.options?.swiperCallback?.onContentDidScroll) {
            this.options.swiperCallback?.onContentDidScroll(selectedIndex, index, position, mainAxisLength);
          }
        });
      }
      .width(this.sliderPlayerSize.width)
      .height(this.sliderPlayerSize.height)
    }
    .width(CommonConstant.FULL_PERCENT_WIDTH)
    .height(CommonConstant.FULL_PERCENT_HEIGHT)
    .alignItems(this.sliderPlayerDirection.horizontalAlign)
  }
}
```

### Patch
```diff
// File: HMSliderPlayer/src/main/ets/components/HMSliderPlayer.ets
--- a/HMSliderPlayer/src/main/ets/components/HMSliderPlayer.ets
+++ b/HMSliderPlayer/src/main/ets/components/HMSliderPlayer.ets
@@ -78,7 +78,7 @@
                 hmAVPlayerMgr: this.hmAVPlayerMgr,
                 hmSliderPlayerController: this.hmSliderPlayerController
               });
-            }, (item: HMSliderPlayerDataSource, index: number) => JSON.stringify(item) + index);
+            }, (item: HMSliderPlayerDataSource, index: number) => index.toString());
         }
         .cachedCount(CommonConstant.DEFAULT_SWIPER_CACHE_COUNT)
         .width(CommonConstant.FULL_PERCENT_WIDTH)


```

## [34/50] ID: OH_0256 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `product/phone/src/main/ets/Setting/IntelligentScene/view/AppSelectedGroupsComponent.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
```typescript
@Component
export struct AppSelectedGroupsComponent {
  private onAppItemClicked: (index: number, item: AppInfo) => void = () => {};
  @Link appGroups: AppInfoDataSource;

  build() {
    Column() {
      List({ space: 0, initialIndex: 0 }) {
        LazyForEach(this.appGroups, (item: AppInfo, index: number) => {
          ListItem() {
            AppListDataInfoComponent({
              item: item,
              index: index,
              totalCount: this.appGroups.totalCount(),
              onAppItemClicked: this.onAppItemClicked,
              isSelectedList: true,
            })
          }
        }, (item: AppInfo) => (`${item.name}${item.isSelected}`))
      }
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring)
      .scrollBar(BarState.Off)
    }
  }
}
```

### Patch
```diff
// File: product/phone/src/main/ets/Setting/IntelligentScene/view/AppSelectedGroupsComponent.ets
--- a/product/phone/src/main/ets/Setting/IntelligentScene/view/AppSelectedGroupsComponent.ets
+++ b/product/phone/src/main/ets/Setting/IntelligentScene/view/AppSelectedGroupsComponent.ets
@@ -36,7 +36,7 @@
               isSelectedList: true,
             })
           }
-        }, (item: AppInfo) => (`${item.name}${item.isSelected}`))
+        }, (item: AppInfo) => (`${item.name}${item.isSelected}`), { cachedCount: 5 })
       }
       .listDirection(Axis.Vertical)
       .edgeEffect(EdgeEffect.Spring)


```

## [35/50] ID: OH_0118 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/contacts/settings/SelectRepeatContact.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
```typescript
@Component
struct ContactsList {
  @Link presenter: ArrangeContactsPresenter;
  private scroller: Scroller = GlobalContext.getContext().getObject('scrollerSelectRepeatContact') as Scroller;
  @State alphabetSelected: number = 0;
  @State isAlphabetClicked: boolean = false;
  @State dragList: boolean = false;
  @StorageProp('fontSizeScale') fontSizeScale: number = 0;
  private isPC: boolean = EnvironmentProp.isPC();
  private slidingMultipleSelectionsUtil: SlidingMultipleSelectionsUtil =
    new SlidingMultipleSelectionsUtil(this.scroller, 56);


  build() {
    Flex({
      direction: FlexDirection.Column,
      justifyContent: FlexAlign.Start,
      alignItems: ItemAlign.Center }) {
      List({ initialIndex: this.presenter.initialIndex, scroller: this.scroller }) {
        LazyForEach(this.presenter.repeatDataSource, (item: RepeatContactVo, index: number) => {
          ListItem() {
            RepeatContactListItem({
              mPresenter: this.presenter,
              item: item,
              index: index
            })
          }
        }, (item: BatchSelectContact) => JSON.stringify(item))
      }
      .width('100%')
      .height('100%')
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
      .scrollBar(BarState.Off)
      .clipContent(ContentClipMode.SAFE_AREA)
      .safeAreaPadding({ top: $r('app.float.id_item_height_max') })
      .onScrollIndex((firstIndex: number, lastIndex: number) => {
        this.slidingMultipleSelectionsUtil.scrollStartIndex = firstIndex;
        this.slidingMultipleSelectionsUtil.scrollEndIndex = lastIndex;

        this.presenter.sceillOnlenth = (lastIndex - firstIndex) + 1
        this.presenter.resetInitialIndex(firstIndex);
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
      .divider({
        strokeWidth: '1px',
        color: $r('app.color.skin_comp_divider'),
        startMargin: $r('app.float.account_listItem_text_common_width'),
        endMargin: this.isPC ? $r('sys.float.padding_level12') : $r('sys.float.padding_level8'),
      })
      .gesture(PanGesture({ direction: PanDirection.Vertical })
        .onActionStart((event: GestureEvent) => {
          for (let i = 0; i < this.presenter.repeatDataSource.totalCount(); ++i) {
            let item = this.presenter.repeatDataSource.getData(i);
            let selectStatus = this.presenter.selectedRepeatContacts.hasKey(item?.repeatId);
            this.slidingMultipleSelectionsUtil.oldSelectStatus[i] = selectStatus;
            this.slidingMultipleSelectionsUtil.curSelectStatus[i] = selectStatus;
          }
          this.slidingMultipleSelectionsUtil.onActionStart(event.fingerList[0]);
        })
        .onActionUpdate((event: GestureEvent) => {
          let updateIndexes = this.slidingMultipleSelectionsUtil.onActionUpdate(event.fingerList[0], (index) => {
            let curSelectStatus = false;
            if (index >= 0) {
              let item = this.presenter.repeatDataSource.getData(index);
              curSelectStatus = this.presenter.selectedRepeatContacts.hasKey(item?.repeatId);
            }
            return curSelectStatus;
          });
          updateIndexes.forEach((index) => {
            if (index >= 0) {
              let item = this.presenter.repeatDataSource.getData(index);
              this.presenter.onItemClick(item, index);
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
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r('app.color.color_bind_sheet_background'))
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/settings/SelectRepeatContact.ets
--- a/entry/src/main/ets/pages/contacts/settings/SelectRepeatContact.ets
+++ b/entry/src/main/ets/pages/contacts/settings/SelectRepeatContact.ets
@@ -412,7 +412,7 @@
               index: index
             })
           }
-        }, (item: BatchSelectContact) => JSON.stringify(item))
+        }, (item: BatchSelectContact) => JSON.stringify(item), { cachedCount: 5 })
       }
       .width('100%')
       .height('100%')


```

## [36/50] ID: OH_0002 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkts-no-use-any-export-other`
- **Result:** `PASS`
- **Target File:** `hadss_dialog/Index.ets`
- **Warning:** Do not use export * to export types and data defined in the other module

###  Buggy Snippet
```typescript
* See the License for the specific language governing permissions and
 * limitations under the License.
 */
export * from './src/main/ets/common/common';

export * from './src/main/ets/model/model';
```

### Patch
```diff
// File: hadss_dialog/Index.ets
--- a/hadss_dialog/Index.ets
+++ b/hadss_dialog/Index.ets
@@ -12,6 +12,42 @@
  * See the License for the specific language governing permissions and
  * limitations under the License.
  */
-export * from './src/main/ets/common/common';
+export { DialogAction } from './src/main/ets/common/common';
+export { DialogBackPressResult } from './src/main/ets/common/common';
+export { DialogType } from './src/main/ets/common/common';
+export { DialogStatus } from './src/main/ets/common/common';
+export { DialogAnimation } from './src/main/ets/common/common';
+export { AnimationType } from './src/main/ets/common/common';
+export { DialogStyle } from './src/main/ets/common/common';
+export { PopupStyle } from './src/main/ets/common/common';
+export { SheetStyle } from './src/main/ets/common/common';
+export { DialogDismissReason } from './src/main/ets/common/common';
+export {
+  DialogConfig,
+  DialogBehavior,
+  DialogLayerPolicy,
+  DialogPosition,
+  DialogMode
+} from './src/main/ets/common/common';
+export { TopDialogPriority } from './src/main/ets/common/common';
+export { PopupConfig, PopupPostion } from './src/main/ets/common/common';
+export { CustomKeyboardAvoidMode } from './src/main/ets/common/common';
+export { SheetBehavior } from './src/main/ets/common/common';
+export { ButtonItemParams } from './src/main/ets/common/common';
+export { SheetItem } from './src/main/ets/common/common';
+export { IconHorizontalToastContent, IconVerticalToastContent } from './src/main/ets/common/common';
+export { IconPosition, PopupItem } from './src/main/ets/common/common';
 
-export * from './src/main/ets/model/model';
+export { DialogHub } from './src/main/ets/model/model';
+export { GlobalEvent } from './src/main/ets/model/model';
+export { InfDialog } from './src/main/ets/model/model';
+export { InfCustomDialog } from './src/main/ets/model/model';
+export { InfPopup } from './src/main/ets/model/model';
+export { InfSheet } from './src/main/ets/model/model';
+export { InfToast } from './src/main/ets/model/model';
+export { DialogLifeCycle } from './src/main/ets/model/model';
+export { SheetLifeCycle } from './src/main/ets/model/model';
+export { PresetCustom } from './src/main/ets/model/model';
+export { PresetPopup } from './src/main/ets/model/model';
+export { PresetSheet } from './src/main/ets/model/model';
+export { PresetToast } from './src/main/ets/model/model';


```

## [37/50] ID: OH_0065 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets`
- **Warning:** Set cachedCount to an appropriate value when using LazyForEach in grids

###  Buggy Snippet
```typescript
@Component
struct ContactsPickerSearch {
  @Link presenter: ContactsPickerPresenter;
  @Prop userId: number;
  @Prop localId: number;
  @Prop maxFontScale: number | null = null;
  @Prop isMultiSelect: boolean;
  @Prop isDisplayByName: boolean;
  @Prop selectedCount: number = 0;
  @Prop verdeSecurityShieldHeight: number
  @Prop isSaveExistContact: boolean;
  @Prop selectedViewShow: boolean;
  @State deleteContact: boolean = false;
  @Link isShowOnlyAccessedAlert: boolean;
  @Link isShowLearnMore: boolean
  @StorageProp('spaceLR') spaceLR: Resource = $r('sys.float.padding_level8');
  @StorageProp('isVerde') isVerde: boolean = false;
  private scroller: Scroller = new Scroller();
  private slidingMultipleSelectionsUtil: SlidingMultipleSelectionsUtil =
    new SlidingMultipleSelectionsUtil(this.scroller, 56);

  aboutToAppear() {
    HiLog.w(TAG, `ContactsPickerSearch aboutToAppear`);
    this.slidingMultipleSelectionsUtil.isSliding = this.isMultiSelect;
  }

  aboutToDisappear() {
    HiLog.w(TAG, `ContactsPickerSearch aboutToDisappear`);
  }


  build() {
    Flex({ direction: FlexDirection.Column }) {
      List({ space: 0, initialIndex: 0, scroller: this.scroller }) {
        LazyForEach(this.presenter.searchContactsSource, (item: ContactPickerListItem, index: number) => {
          ListItem() {
            ContactsPickerListItem({
              presenter: this.presenter,
              userId: this.userId,
              localId: this.localId,
              item: item,
              index: index,
              isMultiSelect: this.isMultiSelect,
              isDisplayByName: this.isDisplayByName,
              isSaveExistContact: this.isSaveExistContact,
              maxFontScale: pickerMaxFontScale,
              customIndexTitle: $r('app.string.contact'),
              isSearch: true,
            })
          }
          .id('ContactSearch_.Contacts_SearchResultClick_ListItem')
        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
      }
      .divider({
        color: $r('app.color.skin_comp_divider'),
        strokeWidth: '1px',
        startMargin: $r('app.float.id_records_divider_margin_left'),
        endMargin: $r('sys.float.padding_level16')
      })
      .scrollBar(BarState.Off)
      .height('100%')
      .width('100%')
      .listDirection(Axis.Vertical)
      .nestedScroll({
        scrollForward: NestedScrollMode.PARALLEL,
        scrollBackward: NestedScrollMode.PARALLEL
      })
      .contentEndOffset(this.isVerde ? this.verdeSecurityShieldHeight : 0)
      .onScrollIndex((firstIndex: number, lastIndex: number) => {
        this.slidingMultipleSelectionsUtil.scrollStartIndex = firstIndex;
        this.slidingMultipleSelectionsUtil.scrollEndIndex = lastIndex;
      })
      .gesture(PanGesture({ direction: PanDirection.Vertical })
        .onActionStart((event: GestureEvent) => {
          for (let i = 0; i < this.presenter.searchContactsSource.totalCount(); ++i) {
            let item = this.presenter.searchContactsSource.getData(i);
            let selectStatus = this.presenter.selectedContactsMap.get(item?.contactId)?.has(
              item?.pickerShowSubData.keyValue) ?? false;
            this.slidingMultipleSelectionsUtil.oldSelectStatus[i] = selectStatus;
            this.slidingMultipleSelectionsUtil.curSelectStatus[i] = selectStatus;
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
            if (index >= 0) {
              let item = this.presenter.searchContactsSource.getData(index);
              curSelectStatus = this.presenter.selectedContactsMap.get(item?.contactId)?.has(
                item?.pickerShowSubData.keyValue) ?? false;
            }
            return curSelectStatus;
          });
          updateIndexes.forEach((index) => {
            if (index >= 0) {
              let item = this.presenter.searchContactsSource.getData(index);
              this.presenter.itemOnClick(
                item?.contactId, item?.pickerShowSubData.keyValue, item?.pickerShowSubData.dataId);
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
    }
    .height('100%')
    .width('100%')
    .backgroundColor($r('app.color.skin_ohos_id_color_panel_bg'))
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets
--- a/entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets
+++ b/entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets
@@ -631,7 +631,7 @@
                 onlyShowChecked: true,
               })
             }
-          }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
+          }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index), { cachedCount: 5 })
         }
         .width('100%')
         .listDirection(Axis.Vertical)
@@ -1318,7 +1318,7 @@
               customIndexTitle: $r('app.string.favorite'),
             })
           }
-        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
+        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index), { cachedCount: 5 })
 
         //遍历位置
         LazyForEach(this.presenter.contactsSource, (item: ContactPickerListItem, index: number) => {
@@ -1335,7 +1335,7 @@
               maxFontScale: pickerMaxFontScale,
             })
           }
-        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
+        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index), { cachedCount: 5 })
       }
       .accessibilityLevel('no')
       .width('100%')
@@ -1692,7 +1692,7 @@
             })
           }
           .id('ContactSearch_.Contacts_SearchResultClick_ListItem')
-        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
+        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index), { cachedCount: 5 })
       }
       .divider({
         color: $r('app.color.skin_comp_divider'),


```

## [38/50] ID: OH_0315 | ArkTS (T)
- **Rule ID:** `@previewer/mandatory-default-value-for-local-initialization`
- **Result:** `PASS`
- **Target File:** `HMRouterExamples/commons/ui_components/src/main/ets/components/NavBar.ets`
- **Warning:** If a component attribute supports local initialization, a valid, runtime-independent default value should be set for it.

###  Buggy Snippet
```typescript
@Component
export struct NavBar {
  @Require private title: string | Resource | undefined;
  private hideBackBtn: boolean = false;
  private backFunction?: () => void;

  build() {
    Row() {
      if (!this.hideBackBtn) {
        Image($r("app.media.back"))
          .width(40)
          .height(40)
          .margin({ right: $r("app.float.vp_8") })
          .onClick(() => {
            if (this.backFunction) {
              this.backFunction()
            } else {
              HMRouterMgr.pop();
            }
          });
      }

      Text(this.title)
        .fontWeight(FontWeight.Bold)
        .fontColor($r("app.color.text_primary"))
        .fontSize($r("app.float.font_title"));
    }.height(56).margin({ left: $r("app.float.vp_16"), right: $r("app.float.vp_16") });
  }
}
```

### Patch
```diff
// File: HMRouterExamples/commons/ui_components/src/main/ets/components/NavBar.ets
--- a/HMRouterExamples/commons/ui_components/src/main/ets/components/NavBar.ets
+++ b/HMRouterExamples/commons/ui_components/src/main/ets/components/NavBar.ets
@@ -17,7 +17,7 @@
 
 @Component
 export struct NavBar {
-  @Require private title: string | Resource | undefined;
+  private title: string | Resource = '';
   private hideBackBtn: boolean = false;
   private backFunction?: () => void;
 


```

## [39/50] ID: OH_0351 | ArkTS (T)
- **Rule ID:** `@performance/foreach-args-check`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/HomePage.ets`
- **Warning:** For performance purposes, set keyGenerator for ForEach.

###  Buggy Snippet
```typescript
@Component
export struct HomePage {
  ListScroller: ListScroller = new ListScroller();
  @State arrayTitle: Title[] = [];
  arrayStr: string[] =
    [TitleConstants.RECOMMEND, TitleConstants.SURROUNDING, TitleConstants.OUT_TRAVEL, TitleConstants.SELF_DRIVING,
      TitleConstants.MOUNTAINEERING, TitleConstants.PARENTING, TitleConstants.FREE_WALKER, TitleConstants.CAMPING];
  @State array: TitleDataSource = new TitleDataSource();
  swiperController: SwiperController = new SwiperController();
  @State selectIndex: number = 0;
  @State menuType: string = '';
  private scroller: Scroller = new Scroller();

  aboutToAppear(): void {
    // 添加标题模拟数据
    for (let i = 0; i < this.arrayStr.length; i++) {
      let title: Title = new Title();
      if (i === 0) {
        title.isSelected = true;
      }
      title.name = this.arrayStr[i];
      this.arrayTitle.push(title);
      this.array.addItem(this.arrayStr[i]);
    }
  }

  build() {
    Column() {
      SearchBarView()

      Scroll(this.scroller) {
        Column() {
          FunctionView()

          // 标题菜单栏没有做组件复用
          List({ scroller: this.ListScroller }) {
            // Tab标题
            ForEach(this.arrayTitle, (title: Title, index: number) => {
              ListItem() {
                TitleView({
                  title: title, clickListener: () => {
                    if (title.isSelected) {
                      return;
                    }
                    // 点击标题时，滑动到指定Index
                    this.ListScroller.scrollToIndex(index, true, ScrollAlign.CENTER)
                    // 点击标题时，Swiper组件跳转到对应的页面
                    this.swiperController.changeIndex(index, true);
                    // 设置标题为选中状态
                    this.arrayTitle[index].isSelected = true;
                    this.arrayTitle[this.selectIndex].isSelected = false;
                    this.selectIndex = index;
                  }
                }).padding({
                  left: index === 0 ? $r('app.integer.nodepool_title_view_padding_left_side') :
                  $r('app.integer.nodepool_title_view_padding_left'),
                  right: index === this.arrayTitle.length - 1 ?
                  $r('app.integer.nodepool_title_view_padding_right_side') :
                  $r('app.integer.nodepool_title_view_padding_right')
                })
              }
            })
          }
          .width(CommonConstants.FULL_PERCENT)
          .scrollBar(BarState.Off)
          .height($r('app.integer.nodepool_title_view_list_height'))
          .listDirection(Axis.Horizontal)

          Swiper(this.swiperController) {
            LazyForEach(this.array, (item: string, index: number) => {
              // 轮播banner和瀑布流做组件复用
              if (this.menuType == 'home') {
                WaterFlowNodeView({ index: index })
              } else {
                WaterFlowView({ index: index })
              }
            }, (title: string) => title)
          }
          .indicator(false)
          .loop(false)
          .onAnimationStart((_index: number, targetIndex: number) => {
            // Swiper滑动切换页面时，改变标题栏的选中状态
            if (this.selectIndex !== targetIndex) {
              this.ListScroller.scrollToIndex(targetIndex, true, ScrollAlign.CENTER)
              this.arrayTitle[targetIndex].isSelected = true;
              this.arrayTitle[this.selectIndex].isSelected = false;
              this.selectIndex = targetIndex;
            }
          })
          .cachedCount(0)
        }
        .justifyContent(FlexAlign.Start);
      }
      .width(CommonConstants.FULL_PERCENT)
      .scrollBar(BarState.Off);
    }
    .backgroundColor($r("app.color.common_background_color"))
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/HomePage.ets
--- a/entry/src/main/ets/pages/HomePage.ets
+++ b/entry/src/main/ets/pages/HomePage.ets
@@ -84,7 +84,7 @@
                   $r('app.integer.nodepool_title_view_padding_right')
                 })
               }
-            })
+            }, (title: Title) => title.name)
           }
           .width(CommonConstants.FULL_PERCENT)
           .scrollBar(BarState.Off)


```

## [40/50] ID: OH_0140 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-transition-to-replace-animateto`
- **Result:** `PASS`
- **Target File:** `product/pc/controlpanel/src/main/ets/pages/index.ets`
- **Warning:** Use transition for component transition animation

###  Buggy Snippet
```typescript
@Component
struct Index {
  @StorageLink('StatusCoefficient') StatusCoefficient: number = 1.0
  @State style: IndexStyle = new IndexStyle()
  @State mBackground: PixelMap | undefined = undefined;
  @State mOpacity: number = 0.0;
  @State mWidthSize: number = 0.2
  @State mHeightSize: number = 0.2
  @State mHeightPx: number = 0
  mClearCallbacks: Array<unsubscribe> = [];
  mShowAnimReady: boolean = false;

  aboutToAppear() {
    Log.showInfo(TAG, `aboutToAppear, start`)

    setAppBgColor('#00000000')
    CommonStyleManager.setAbilityPageName(TAG)
    this.style = StyleConfiguration.getIndexStyle()
    StyleManager.setStyle()

    let rect = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_CONTROL_PANEL, 'rect')
    this.mHeightPx = rect.height

    mHeightConfigUtils = new HeightConfigUtils();
    let StatusCoefficient;

    StatusCoefficient = AppStorage.SetAndLink("StatusCoefficient", 1.0);
    StatusCoefficient.set(mHeightConfigUtils.getStatusCoefficient());

    this.initWindowPolicy();
    Log.showDebug(TAG, `aboutToAppear, end`)
  }

  onPageShow() {
    this.showAnimation();
  }

  aboutToDisappear() {
    Log.showInfo(TAG, `aboutToDisappear`)
    this.mClearCallbacks.forEach((unsubscribe) => unsubscribe());
    this.mClearCallbacks.length = 0;
  }

  build() {
    Column(){
      Stack({ alignContent: Alignment.Top }) {
        Image(this.mBackground)
          .width('100%')
          .height('100%')
          .objectFit(ImageFit.Fill)
        Scroll(new Scroller()) {
          Column() {
            ControlCenterComponent({
              modeChangeCallback: (isEdit) => this.onModeChange(isEdit)
            })
          }
          .width('100%')
          .onAreaChange((e, e2) => {
            Log.showInfo(TAG, `onAreaChange, e: ${JSON.stringify(e)} e2: ${JSON.stringify(e2)}`);
          })
        }
        .scrollBarColor(Color.Gray)
        .scrollBarWidth(10)
        .width('100%')
        .height('100%')
        .backgroundColor($r('app.color.default_background'))
      }
      .scale({
        x: this.mWidthSize,
        y: this.mHeightSize,
        z: 1,
        centerX: '100%',
        centerY: '0%'
      })
      .opacity(this.mOpacity)
      .clip(true)
      .borderRadius(this.style.borderRadius)
      .width('97%')
      .height(0.97 * this.mHeightPx + 'px')
    }
    .width('100%')
    .height('100%')
    .alignItems(HorizontalAlign.End)
  }

  initWindowPolicy() {
    Log.showDebug(TAG, `init controlcenter panel window Policy`);
    this.mClearCallbacks.push(
    EventManager.subscribe(SHOW_EVENT, () => WindowManager.showWindow(WindowType.CONTROL_PANEL)),
    EventManager.subscribe(HIDE_EVENT, () => this.hideWindow()),
    EventManager.subscribe(START_ABILITY_EVENT, () => this.hideWindow()),
    EventManager.subscribe(WINDOW_SHOW_HIDE_EVENT, (args) => {
      let { windowName, isShow } = args;
      Log.showInfo(TAG, `WINDOW_SHOW_HIDE_EVENT windowName: ${windowName}, isShow: ${isShow}`);
      windowName == WindowType.NOTIFICATION_PANEL && isShow && this.hideWindow();
      windowName == WindowType.CONTROL_PANEL && isShow && (this.mShowAnimReady = true);
    }),
    EventManager.subscribe('ControlWindowResizeEvent',async (args) => {
      let { windowName, rect } = args;
      let dis = await display.getDefaultDisplay();
      Log.showInfo(TAG, `ControlWindowResizeEvent: ${windowName}, isShow: ${rect}`);
      AbilityManager.setAbilityData(AbilityManager.ABILITY_NAME_CONTROL_PANEL, 'rect', rect);
      AbilityManager.setAbilityData(AbilityManager.ABILITY_NAME_CONTROL_PANEL, 'dis', {
        width: dis.width,
        height: dis.height,
      });
      WindowManager.resetSizeWindow(windowName, rect).then(
      ).then(() => {
      }).catch((err) => {
      });
    }),
    MultimodalInputManager.subscribeCombinationKey([MultiKeyCode.WIN, MultiKeyCode.I], (data) => {
      let windowInfo = WindowManager.getWindowInfo(WindowType.CONTROL_PANEL);
      Log.showInfo(TAG, `on CombinationKeyEvent: data: ${data}, windowInfo: ${windowInfo?.visibility}`);
      if (windowInfo) {
          windowInfo.visibility
          ? this.hideWindow()
          : WindowManager.showWindow(WindowType.CONTROL_PANEL);
      }
    })
    );
  }

  _animateTo(config, callback) {
    animateTo(config, callback)
    setTimeout(config.onFinish, config.duration + config.delay)
  }

  showAnimation(){

    //init page state
    this.mOpacity = 0;
    this.mWidthSize = 0.7;
    this.mHeightSize = 0.7;

    //show animation
    animateTo({
      duration: 200,
      curve: Curve.Friction
    }, () => {
      this.mOpacity = 1;
      this.mWidthSize = 1.03;
      this.mHeightSize = 1.03;
    })
    animateTo({
      duration:100,
      curve: Curve.Friction,
      delay: 200
    }, () =>{
      this.mWidthSize = 1;
      this.mHeightSize = 1;
    })
  }

  hideAnimation(){
    //hide animation
    animateTo({
      duration: 100,
      curve: Curve.Friction,
      onFinish: () => {
        WindowManager.hideWindow(WindowType.CONTROL_PANEL);
      }
    }, () => {
      this.mWidthSize = 0.7;
      this.mHeightSize = 0.7;
      this.mOpacity = 0;
    })
  }

  hideWindow() {
    this.hideAnimation();
  }

  onModeChange(isEdit) {
    Log.showDebug(TAG, `onModeChange, isEdit: ${isEdit}`)
    let initRect = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_CONTROL_PANEL, 'rect')
    let newRect = initRect
    if (isEdit) {
      let dis = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_CONTROL_PANEL, 'dis')
      newRect = { ...initRect, height: StyleManager.calcScaleSize(346) }
    }
    Log.showDebug(TAG, `onModeChange, newRect: ${JSON.stringify(newRect)}`)
    this._animateTo({
      duration: 300,
      tempo: 1.0,
      curve: Curve.Friction,
      delay: 0,
      iterations: 1,
      playMode: PlayMode.Normal,
      onFinish: () => {
        Log.showInfo(TAG, `onModeChange, show anim finish.`)
        if (newRect.height <= initRect.height) {
          WindowManager.resetSizeWindow(WindowType.CONTROL_PANEL, newRect)
        }
      }
    }, () => {
      Log.showInfo(TAG, `onModeChange, animateTo`)
      if (newRect.height > initRect.height) {
        WindowManager.resetSizeWindow(WindowType.CONTROL_PANEL, newRect)
      }
      this.mHeightPx = newRect.height
    })
  }
}
```

### Patch
```diff
// File: product/pc/controlpanel/src/main/ets/pages/index.ets
--- a/product/pc/controlpanel/src/main/ets/pages/index.ets
+++ b/product/pc/controlpanel/src/main/ets/pages/index.ets
@@ -46,6 +46,7 @@
   @State mWidthSize: number = 0.2
   @State mHeightSize: number = 0.2
   @State mHeightPx: number = 0
+  @State isVisible: boolean = false;
   mClearCallbacks: Array<unsubscribe> = [];
   mShowAnimReady: boolean = false;
 
@@ -116,6 +117,10 @@
       .borderRadius(this.style.borderRadius)
       .width('97%')
       .height(0.97 * this.mHeightPx + 'px')
+      .animation({ duration: 300, curve: Curve.Friction })
+      .transition(TransitionEffect.OPACITY.animation({ duration: 200, curve: Curve.Friction })
+        .combine(TransitionEffect.scale({ x: 0.7, y: 0.7, z: 1, centerX: '100%', centerY: '0%' })
+          .animation({ duration: 200, curve: Curve.Friction })))
     }
     .width('100%')
     .height('100%')
@@ -160,11 +165,6 @@
     );
   }
 
-  _animateTo(config, callback) {
-    animateTo(config, callback)
-    setTimeout(config.onFinish, config.duration + config.delay)
-  }
-
   showAnimation(){
 
     //init page state
@@ -172,38 +172,26 @@
     this.mWidthSize = 0.7;
     this.mHeightSize = 0.7;
 
-    //show animation
-    animateTo({
-      duration: 200,
-      curve: Curve.Friction
-    }, () => {
-      this.mOpacity = 1;
-      this.mWidthSize = 1.03;
-      this.mHeightSize = 1.03;
-    })
-    animateTo({
-      duration:100,
-      curve: Curve.Friction,
-      delay: 200
-    }, () =>{
+    //show animation - using state changes with transition
+    this.mOpacity = 1;
+    this.mWidthSize = 1.03;
+    this.mHeightSize = 1.03;
+    
+    setTimeout(() => {
       this.mWidthSize = 1;
       this.mHeightSize = 1;
-    })
+    }, 200);
   }
 
   hideAnimation(){
-    //hide animation
-    animateTo({
-      duration: 100,
-      curve: Curve.Friction,
-      onFinish: () => {
-        WindowManager.hideWindow(WindowType.CONTROL_PANEL);
-      }
-    }, () => {
-      this.mWidthSize = 0.7;
-      this.mHeightSize = 0.7;
-      this.mOpacity = 0;
-    })
+    //hide animation - using state changes with transition
+    this.mWidthSize = 0.7;
+    this.mHeightSize = 0.7;
+    this.mOpacity = 0;
+    
+    setTimeout(() => {
+      WindowManager.hideWindow(WindowType.CONTROL_PANEL);
+    }, 100);
   }
 
   hideWindow() {
@@ -219,25 +207,19 @@
       newRect = { ...initRect, height: StyleManager.calcScaleSize(346) }
     }
     Log.showDebug(TAG, `onModeChange, newRect: ${JSON.stringify(newRect)}`)
-    this._animateTo({
-      duration: 300,
-      tempo: 1.0,
-      curve: Curve.Friction,
-      delay: 0,
-      iterations: 1,
-      playMode: PlayMode.Normal,
-      onFinish: () => {
-        Log.showInfo(TAG, `onModeChange, show anim finish.`)
-        if (newRect.height <= initRect.height) {
-          WindowManager.resetSizeWindow(WindowType.CONTROL_PANEL, newRect)
-        }
-      }
-    }, () => {
-      Log.showInfo(TAG, `onModeChange, animateTo`)
-      if (newRect.height > initRect.height) {
+    
+    // Use state change with transition instead of animateTo
+    Log.showInfo(TAG, `onModeChange, animateTo`)
+    if (newRect.height > initRect.height) {
+      WindowManager.resetSizeWindow(WindowType.CONTROL_PANEL, newRect)
+    }
+    this.mHeightPx = newRect.height
+    
+    setTimeout(() => {
+      Log.showInfo(TAG, `onModeChange, show anim finish.`)
+      if (newRect.height <= initRect.height) {
         WindowManager.resetSizeWindow(WindowType.CONTROL_PANEL, newRect)
       }
-      this.mHeightPx = newRect.height
-    })
+    }, 300);
   }
 }


```

## [41/50] ID: OH_0370 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkts-no-use-any-export-other`
- **Result:** `PASS`
- **Target File:** `rocketchat/Index.ets`
- **Warning:** Do not use export * to export types and data defined in the other module

###  Buggy Snippet
```typescript
*/

import router from '@ohos.router';


export * from './src/main/ets/components/rest/RestAPI'
```

### Patch
```diff
// File: rocketchat/Index.ets
--- a/rocketchat/Index.ets
+++ b/rocketchat/Index.ets
@@ -16,4 +16,4 @@
 import router from '@ohos.router';
 
 
-export * from './src/main/ets/components/rest/RestAPI'
+export { RestAPI } from './src/main/ets/components/rest/RestAPI'


```

## [42/50] ID: OH_0064 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/contacts/batchselectcontacts/ContactsPickerPage.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
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
@@ -631,7 +631,7 @@
                 onlyShowChecked: true,
               })
             }
-          }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
+          }, (item: ContactPickerListItem, index: number) => `${item.contactId}_${item.pickerShowSubData.keyValue}_${index}`)
         }
         .width('100%')
         .listDirection(Axis.Vertical)
@@ -1318,7 +1318,7 @@
               customIndexTitle: $r('app.string.favorite'),
             })
           }
-        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
+        }, (item: ContactPickerListItem, index: number) => `${item.contactId}_${item.pickerShowSubData.keyValue}_${index}`)
 
         //遍历位置
         LazyForEach(this.presenter.contactsSource, (item: ContactPickerListItem, index: number) => {
@@ -1335,7 +1335,7 @@
               maxFontScale: pickerMaxFontScale,
             })
           }
-        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
+        }, (item: ContactPickerListItem, index: number) => `${item.contactId}_${item.pickerShowSubData.keyValue}_${index}`)
       }
       .accessibilityLevel('no')
       .width('100%')
@@ -1692,7 +1692,7 @@
             })
           }
           .id('ContactSearch_.Contacts_SearchResultClick_ListItem')
-        }, (item: ContactPickerListItem, index: number) => JSON.stringify(item) + JSON.stringify(index))
+        }, (item: ContactPickerListItem, index: number) => `${item.contactId}_${item.pickerShowSubData.keyValue}_${index}`)
       }
       .divider({
         color: $r('app.color.skin_comp_divider'),
@@ -1927,7 +1927,7 @@
                           .fontColor($r('app.color.skin_ohos_fa_text_primary'))
                       }
                     }
-                  }, (item: string, index: number) => JSON.stringify(item) + JSON.stringify(index))
+                  }, (item: string, index: number) => `${item}_${index}`)
               }
             }
             .fontColor($r('app.color.skin_font_primary'))
@@ -1954,8 +1954,7 @@
                   Span(item)
                     .fontColor($r('app.color.skin_ohos_fa_text_primary'))
                 }
-              }, (item: string, index: number) => JSON.stringify(this.item.pickerShowSubData.showValue as string) +
-              JSON.stringify(index) + this.item.highLight?.toString())
+              }, (item: string, index: number) => `${this.item.pickerShowSubData.showValue}_${index}_${this.item.highLight?.toString()}`)
             }
             .textAlign(i18n.isRTL(i18n.System.getSystemLanguage()) ? TextAlign.End : TextAlign.Start)
             .direction(Direction.Ltr)


```

## [43/50] ID: OH_0347 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-object-link-to-replace-prop`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/view/ItemDescView/DescRaidersView.ets`
- **Warning:** Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

###  Buggy Snippet
```typescript
@Component
export struct DescRaidersView {
  @Prop item: ViewItem = new ViewItem();
  private numberFormat: intl.NumberFormat = new intl.NumberFormat('collectionsCount', { maximumFractionDigits: 1 });
  @Prop @Watch('onIsLikeChange') isLike: boolean = false;
  @State flag: boolean = false;
  @State likeCount: number = this.item.likeCount;

  onIsLikeChange() {
    this.flag = this.isLike;
    if (this.flag) {
      this.item.likeCount++;
    } else {
      this.item.likeCount--;
    }
  }

  build() {
    Column() {
      Text(this.item.title)
        .fontSize($r('app.float.title_font'))
        .fontWeight(CommonConstants.TEXT_FONT_WEIGHT_500)
        .width(CommonConstants.FULL_PERCENT)
        .maxLines(CommonConstants.TEXT_MAX_LINES)
        .textOverflow({ overflow: TextOverflow.Ellipsis });

      Row() {
        Row() {
          Image(this.item.userIcon)
            .width($r('app.float.image_size_16'))
            .height($r('app.float.image_size_16'))
            .borderRadius($r('app.float.image_size_16'))
            .margin({ right: $r('app.float.margin_5') })
          Text(this.item.userName)
            .fontSize($r('app.float.font_10'))
            .fontWeight(CommonConstants.TEXT_FONT_WEIGHT_400)
            .fontColor(Color.Black)
            .opacity(0.6)
        }
        .justifyContent(FlexAlign.Center);

        Blank();

        Row() {
          Image(this.flag ? $r('app.media.like') : $r('app.media.ic_public_heart'))
            .fillColor(Color.Black)
            .objectFit(ImageFit.Fill)
            .width($r('app.float.image_size_16'))
            .height($r('app.float.image_size_16'))

          Text(this.item.likeCount < 1000 ? this.item.likeCount + '' :
            this.numberFormat.format(this.item.likeCount / 1000) + 'k')
            .fontSize($r('app.float.font_12'))
            .fontFamily($r('sys.string.ohos_id_text_font_family_regular'))
            .fontColor(Color.Black)
            .opacity(0.6)
            .margin({ left: $r('app.float.margin_4') });
        };
      }
      .justifyContent(FlexAlign.SpaceBetween)
      .width(CommonConstants.FULL_PERCENT)
      .margin({ top: $r('app.float.margin_8') });

      Row() {
        Image($r('app.media.rank_icon'))
          .width($r('app.float.image_size_12'))
          .height($r('app.float.image_size_12'))
          .margin({ left: $r('app.float.margin_10'), top: $r('app.float.margin_4'), bottom: $r('app.float.margin_4') })
        Text('全国古镇第一名')
          .fontSize($r('app.float.title_font'))
          .fontColor($r('app.color.raider_rank_font_color'))
          .margin(
            {
              left: $r('app.float.margin_5'),
              right: $r('app.float.margin_10'),
              top: $r('app.float.margin_2'),
              bottom: $r('app.float.margin_2')
            }
          )
      }
      .margin({ bottom: $r('app.float.margin_5'), top: $r('app.float.margin_8') })
      .backgroundColor($r('app.color.raider_rank_background_color'))
      .justifyContent(FlexAlign.Center)
      .borderRadius($r('app.float.common_border_radius_4'))
    }
    .alignItems(HorizontalAlign.Start)
    .padding({
      left: $r('app.float.padding_12'),
      right: $r('app.float.padding_12'),
      top: $r('app.float.padding_12'),
      bottom: $r('app.float.padding_10')
    })
    .width(CommonConstants.FULL_PERCENT);
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/view/ItemDescView/DescRaidersView.ets
--- a/entry/src/main/ets/view/ItemDescView/DescRaidersView.ets
+++ b/entry/src/main/ets/view/ItemDescView/DescRaidersView.ets
@@ -19,7 +19,7 @@
 
 @Component
 export struct DescRaidersView {
-  @Prop item: ViewItem = new ViewItem();
+  @ObjectLink item: ViewItem;
   private numberFormat: intl.NumberFormat = new intl.NumberFormat('collectionsCount', { maximumFractionDigits: 1 });
   @Prop @Watch('onIsLikeChange') isLike: boolean = false;
   @State flag: boolean = false;


```

## [44/50] ID: OH_0139 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-suggest-use-effectkit-blur`
- **Result:** `PASS`
- **Target File:** `product/phone/dropdownpanel/src/main/ets/pages/index.ets`
- **Warning:** Suggestion Use effectKit.createEffect to create a blur effect

###  Buggy Snippet
```typescript
@Component
struct Index {
  @State showComponentName: string = undefined
  @State componentOptAreaHeightPX: number = 0
  @StorageLink('StatusCoefficient') StatusCoefficient: number = 1.0
  mCallback: any;
  mClearCallbacks: unsubscribe[]
  settingDataKey = 'settings.display.navigationbar_status';
  urivar: string = null;
  helper: any = null;
  mNavigationBarStatusDefaultValue: string = '1';
  navigationBarWidth: number = 0;
  mNeedUpdate: boolean = false;
  mWidthPx: number = 0;
  @State mNotificationInsert: any = {}
  @State mNotificationDelete: any = {}
  @State mControlCenterInsert: any = {}
  @State mControlCenterDelete: any = {}
  @State componentOptAreaTranslateY: string = '0px'
  @State backgroundOpacity: number = 0

  onBackPress(): boolean {
    return true
  }

  aboutToAppear() {
    Log.showInfo(TAG, `aboutToAppear, start`)

    setAppBgColor('#00000000')
    CommonStyleManager.setAbilityPageName(TAG)
    StyleManager.setStyle()

    let dropdownRect = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_DROPDOWN_PANEL, 'rect')
    let navigationBarRect = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_NAVIGATION_BAR, 'config')
    this.urivar = settings.getUriSync(this.settingDataKey);
    this.helper = featureAbility.acquireDataAbilityHelper(AbilityManager.getContext(), CommonConstants.URI_VAR);
    this.resizeDropdownPanelAndNavigationBar(dropdownRect, navigationBarRect);
    Log.showDebug(TAG, `getValueSync componentOptAreaHeightPX: ${this.componentOptAreaHeightPX}`)
    this.helper.on("dataChange", this.urivar, (data) => {
      if (data.code !== 0) {
        Log.showError(TAG, `dataChangesCallback failed, because ${data.message}`);
        return;
      } else {
        this.resizeDropdownPanelAndNavigationBar(dropdownRect, navigationBarRect);
        Log.showInfo(TAG, `NavigationBar status change, componentOptAreaHeightPX: ${this.componentOptAreaHeightPX}`)
      }
    })

    this.componentOptAreaTranslateY = (-this.componentOptAreaHeightPX * 0.1) + 'px'

    this.mClearCallbacks = []
    this.mClearCallbacks.push(
    EventManager.subscribe('DropdownEvent', (args) => this.onDropdownEvent(args)),
    EventManager.subscribe(START_ABILITY_EVENT, (args) => this.onStartAbility(args)),
    EventManager.subscribe('hideNotificationWindowEvent', (args) => this.onHideNotificationWindowEvent(args)))

    mHeightConfigUtils = new HeightConfigUtils();
    let StatusCoefficient;

    StatusCoefficient = AppStorage.SetAndLink("StatusCoefficient", 1.0);
    StatusCoefficient.set(mHeightConfigUtils.getStatusCoefficient());

    let signalObserved = AppStorage.SetAndLink("signalObserved", false);
    signalObserved.set(false);

    this.mCallback = {
      "onStateChange": (data) => this.onStateChange(data),
      "onNotificationShowOrHide": (data) => this.onNotificationShowOrHide(data),
      "onControlShowOrHide": (data) => this.onControlShowOrHide(data)
    }
    NavigationEvent.registerCallback(this.mCallback);
    MultimodalInputManager.registerControlListener(this.mCallback);
    MultimodalInputManager.registerNotificationListener(this.mCallback);
    Log.showDebug(TAG, `aboutToAppear, end`)
  }

  onPageShow() {
    Log.showInfo(TAG, `onPageShow, start`)
    if (!this.showComponentName) {
      return
    }
    StatusBarVM.setUseInWindowName(WindowType.DROPDOWN_PANEL)
    this.componentOptAreaTranslateY = '0px'
    this.backgroundOpacity = 1
    Trace.end(Trace.CORE_METHOD_START_DROPDOWNPANEL)
  }

  aboutToDisappear() {
    Log.showInfo(TAG, `aboutToDisappear`)
    this.mClearCallbacks.forEach((mClearCallback: Function) => {
      mClearCallback()
      mClearCallback = undefined
    })
    this.mClearCallbacks = undefined
  }

  resizeDropdownPanelAndNavigationBar(dropdownRect, navigationBarRect) {
    Log.showDebug(TAG, `resizeDropdownPanelAndNavigationBar, dropdownRect: ${JSON.stringify(dropdownRect)} navigationBarRect: ${JSON.stringify(navigationBarRect)}`)
    this.mNavigationBarStatusDefaultValue = settings.getValueSync(this.helper, this.settingDataKey, '1');
    this.componentOptAreaHeightPX = this.mNavigationBarStatusDefaultValue == '1' ? dropdownRect.height - navigationBarRect.realHeight : dropdownRect.height;
    this.navigationBarWidth = this.mNavigationBarStatusDefaultValue == '1' ? navigationBarRect.height : 0;
    WindowManager.resetSizeWindow(WindowType.NAVIGATION_BAR, { ...navigationBarRect, height: this.navigationBarWidth })
    WindowManager.resetSizeWindow(WindowType.DROPDOWN_PANEL, { ...dropdownRect, height: this.componentOptAreaHeightPX })
  }

  onNotificationShowOrHide(data) {
    Log.showDebug(TAG, `mNotificationAsyncCallback preKeys: ${data.preKeys}, finalKey: ${data.finalKey}`);
    Log.showDebug(TAG, `this.showComponentName: ${this.showComponentName}`);
    if (this.showComponentName == 'Notification') {
      this.hideSelf();
    } else {
      this.showSelf('Notification');
    }
    Log.showDebug(TAG, `mNotificationAsyncCallback end`);
  }

  onControlShowOrHide(data) {
    Log.showDebug(TAG, `mControlAsyncCallback preKeys: ${data.preKeys}, finalKey: ${data.finalKey}`);
    Log.showDebug(TAG, `this.showComponentName: ${this.showComponentName}`);
    if (this.showComponentName == 'ControlCenter') {
      this.hideSelf();
    } else {
      this.showSelf('ControlCenter');
    }
    Log.showDebug(TAG, `mControlAsyncCallback end`);
  }

  onStateChange(data) {
    Log.showDebug(TAG, `onStateChange, data: ${JSON.stringify(data)}`)
    Log.showDebug(TAG, `onStateChange, showComponentName: ${this.showComponentName}`)
    if (this.showComponentName) {
      this.hideSelf()
    }
  }

  onDropdownEvent(args) {
    Log.showDebug(TAG, `onDropdownEvent, args: ${JSON.stringify(args)}`)
    this.showSelf(args.dropdownArea == 'left' ? 'Notification' : 'ControlCenter')
  }

  onStartAbility(args) {
    Log.showDebug(TAG, `onStartAbility, args: ${args}`)
    this.hideSelf()
  }

  onHideNotificationWindowEvent(args) {
    Log.showDebug(TAG, `onHideNotificationWindowEvent, args: ${args}`)
    this.hideSelf()
  }

  onTouchMove(data) {
    Log.showDebug(TAG, `onTouchMove, data: ${JSON.stringify(data)}`)
    if (data.direction == 'top') {
      this.hideSelf()
    } else if (data.direction == 'left' && data.touchComponent == 'notification') {
      this.switchNotificationOrControlCenter('ControlCenter')
    } else if (data.direction == 'right' && data.touchComponent == 'control') {
      this.switchNotificationOrControlCenter('Notification')
    } else if (data.direction == 'drop_left' && data.touchComponent == 'control') {
      this.showComponentName = 'Notification'
    } else if (data.direction == 'drop_right' && data.touchComponent == 'notification') {
      this.showComponentName = 'ControlCenter'
    }
  }

  switchNotificationOrControlCenter(showComponentName) {
    Log.showDebug(TAG, `switchNotificationOrControlCenter, showComponentName: ${showComponentName}`)
    this.mNotificationInsert = { type: TransitionType.Insert, opacity: 0, translate: { x: (-this.mWidthPx) + 'px' } }
    this.mControlCenterInsert = { type: TransitionType.Insert, opacity: 0, translate: { x: (this.mWidthPx) + 'px' } }
    let transitionDelete = {
      type: TransitionType.Delete,
      opacity: 0,
      scale: { x: 0.8, y: 0.8, centerX: '50%', centerY: '50%' }
    }
    this.mNotificationDelete = transitionDelete
    this.mControlCenterDelete = transitionDelete
    this._animateTo({ ...SHOW_ANIM_CONFIG, onFinish: () => {
      Log.showInfo(TAG, `switchNotificationOrControlCenter, show anim finish.`);
    } }, () => {
      this.showComponentName = showComponentName
    })
  }

  showSelf(showComponentName) {
    Trace.end(Trace.CORE_METHOD_START_TOUCHEVENT)
    Log.showDebug(TAG, `showSelf, showComponentName: ${showComponentName}`)
    this.showComponentName = showComponentName
    WindowManager.showWindow(WindowType.DROPDOWN_PANEL)
    Trace.start(Trace.CORE_METHOD_START_DROPDOWNPANEL)
  }

  hideSelf() {
    Log.showDebug(TAG, `hideSelf`)
    this._animateTo({ ...SHOW_ANIM_CONFIG, onFinish: () => {
      Log.showInfo(TAG, `hideSelf, hide anim finish.`);
      this.showComponentName = undefined
      WindowManager.hideWindow(WindowType.DROPDOWN_PANEL)
    } }, () => {
      this.componentOptAreaTranslateY = (-this.componentOptAreaHeightPX * 0.1) + 'px'
      this.backgroundOpacity = 0
    })
  }

  _animateTo(config, callback) {
    Log.showDebug(TAG, `_animateTo, config: ${JSON.stringify(config)}`)
    animateTo(config, callback)
    setTimeout(config.onFinish, config.duration + config.delay)
  }

  build() {
    Stack({ alignContent: Alignment.Top }) {
      Image($r("app.media.dropdownpanel_bgc"))
        .width('100%')
        .height('100%')
        .objectFit(ImageFit.Fill)
        .blur(25)
        .opacity(this.backgroundOpacity)
      Column() {
        if (this.showComponentName == 'Notification') {
          Column() {
            Notification({ touchMoveCallback: (data) => this.onTouchMove(data) })
          }
          .width('100%')
          .height('100%')
          .transition(this.mNotificationInsert)
          .transition(this.mNotificationDelete)
        } else if (this.showComponentName == 'ControlCenter') {
          Column() {
            ControlCenterComponent({
              touchMoveCallback: (data) => this.onTouchMove(data)
            })
          }
          .width('100%')
          .height('100%')
          .transition(this.mControlCenterInsert)
          .transition(this.mControlCenterDelete)
        }
      }
      .width('100%')
      .height(this.componentOptAreaHeightPX + 'px')
      .translate({ y: this.componentOptAreaTranslateY })
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r("app.color.default_background"))
    .opacity(this.backgroundOpacity)
    .onAreaChange((e, e2) => {
      Log.showInfo(TAG, `onAreaChange, e: ${JSON.stringify(e)} e2: ${JSON.stringify(e2)}`);
      this.mWidthPx = vp2px(Number(e2.width))
    })
  }
}
```

### Patch
```diff
// File: product/phone/dropdownpanel/src/main/ets/pages/index.ets
--- a/product/phone/dropdownpanel/src/main/ets/pages/index.ets
+++ b/product/phone/dropdownpanel/src/main/ets/pages/index.ets
@@ -23,6 +23,7 @@
 import RingModeIcon from '../../../../../../../features/ringmodecomponent/src/main/ets/com/ohos/pages/StatusBarIconItemRingModeComponent'
 
 import image from "@ohos.multimedia.image"
+import effectKit from '@ohos.effectKit'
 import Log from '../../../../../../../common/src/main/ets/default/Log'
 import Trace from '../../../../../../../common/src/main/ets/default/Trace'
 import WindowManager, { WindowType, WINDOW_SHOW_HIDE_EVENT
@@ -84,6 +85,7 @@
   @State mControlCenterDelete: any = {}
   @State componentOptAreaTranslateY: string = '0px'
   @State backgroundOpacity: number = 0
+  @State blurPixelMap: PixelMap = undefined
 
   onBackPress(): boolean {
     return true
@@ -137,7 +139,27 @@
     NavigationEvent.registerCallback(this.mCallback);
     MultimodalInputManager.registerControlListener(this.mCallback);
     MultimodalInputManager.registerNotificationListener(this.mCallback);
+    
+    this.createBlurEffect();
     Log.showDebug(TAG, `aboutToAppear, end`)
+  }
+
+  async createBlurEffect() {
+    try {
+      const context = getContext(this);
+      const resourceMgr = context.resourceManager;
+      const fileData = await resourceMgr.getMediaContent($r("app.media.dropdownpanel_bgc").id);
+      const buffer = fileData.buffer;
+      const imageSource = image.createImageSource(buffer);
+      const pixelMap = await imageSource.createPixelMap();
+      const effectFilter = effectKit.createEffect(pixelMap);
+      if (effectFilter) {
+        effectFilter.blur(25);
+        this.blurPixelMap = await effectFilter.getPixelMap();
+      }
+    } catch (err) {
+      Log.showError(TAG, `createBlurEffect failed: ${err}`);
+    }
   }
 
   onPageShow() {
@@ -275,12 +297,19 @@
 
   build() {
     Stack({ alignContent: Alignment.Top }) {
-      Image($r("app.media.dropdownpanel_bgc"))
-        .width('100%')
-        .height('100%')
-        .objectFit(ImageFit.Fill)
-        .blur(25)
-        .opacity(this.backgroundOpacity)
+      if (this.blurPixelMap) {
+        Image(this.blurPixelMap)
+          .width('100%')
+          .height('100%')
+          .objectFit(ImageFit.Fill)
+          .opacity(this.backgroundOpacity)
+      } else {
+        Image($r("app.media.dropdownpanel_bgc"))
+          .width('100%')
+          .height('100%')
+          .objectFit(ImageFit.Fill)
+          .opacity(this.backgroundOpacity)
+      }
       Column() {
         if (this.showComponentName == 'Notification') {
           Column() {


```

## [45/50] ID: OH_0369 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkts-no-use-any-export-other`
- **Result:** `PASS`
- **Target File:** `rocketchat/index.ets`
- **Warning:** Do not use export * to export types and data defined in the other module

###  Buggy Snippet
```typescript
* distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
export * from './src/main/ets/components/rest/RestAPI'
```

### Patch
```diff
// File: rocketchat/index.ets
--- a/rocketchat/index.ets
+++ b/rocketchat/index.ets
@@ -12,4 +12,4 @@
  * See the License for the specific language governing permissions and
  * limitations under the License.
  */
-export * from './src/main/ets/components/rest/RestAPI'
+export { RestAPI } from './src/main/ets/components/rest/RestAPI'


```

## [46/50] ID: OH_0348 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-object-link-to-replace-prop`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/view/ItemDescView/DescTravelImageView.ets`
- **Warning:** Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

###  Buggy Snippet
```typescript
@Component
export struct DescTravelImageView {
  @Prop item: ViewItem = new ViewItem();
  private numberFormat: intl.NumberFormat = new intl.NumberFormat('collectionsCount', { maximumFractionDigits: 1 });
  @Prop @Watch('onIsLikeChange') isLike: boolean = false;
  @State flag: boolean = false;
  @State likeCount: number = this.item.likeCount;

  onIsLikeChange() {
    this.flag = this.isLike;
    if (this.flag) {
      this.item.likeCount++;
    } else {
      this.item.likeCount--;
    }
  }

  build() {
    Column() {
      Text(this.item.title)
        .fontSize($r('app.float.title_font'))
        .fontWeight(CommonConstants.TEXT_FONT_WEIGHT_500)
        .width(CommonConstants.FULL_PERCENT)
        .maxLines(CommonConstants.TEXT_MAX_LINES)
        .textOverflow({ overflow: TextOverflow.Ellipsis });

      Row() {
        Row() {
          Image(this.item.userIcon)
            .width($r('app.float.image_size_16'))
            .height($r('app.float.image_size_16'))
            .borderRadius($r('app.float.common_border_radius_4'))
            .margin({ right: $r('app.float.margin_5') })
          Text(this.item.userName)
            .fontSize($r('app.float.font_10'))
            .fontWeight(CommonConstants.TEXT_FONT_WEIGHT_400)
            .fontColor(Color.Black)
            .opacity(0.6)
        }
        .justifyContent(FlexAlign.Center);

        Blank();

        Row() {
          Image(this.flag ? $r('app.media.like') : $r('app.media.ic_public_heart'))
            .fillColor(Color.Black)
            .objectFit(ImageFit.Fill)
            .width($r('app.float.image_size_16'))
            .height($r('app.float.image_size_16'))

          Text(this.item.likeCount < 1000 ? this.item.likeCount + '' :
            this.numberFormat.format(this.item.likeCount / 1000) + 'k')
            .fontSize($r('app.float.font_12'))
            .fontFamily($r('sys.string.ohos_id_text_font_family_regular'))
            .fontColor(Color.Black)
            .opacity(0.6)
            .margin({ left: $r('app.float.margin_4') });
        };
      }
      .justifyContent(FlexAlign.SpaceBetween)
      .width(CommonConstants.FULL_PERCENT)
      .margin({ top: $r('app.float.margin_8') });
    }
    .padding({
      left: $r('app.float.padding_12'),
      right: $r('app.float.padding_12'),
      top: $r('app.float.padding_12'),
      bottom: $r('app.float.padding_10')
    })
    .width(CommonConstants.FULL_PERCENT);
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/view/ItemDescView/DescTravelImageView.ets
--- a/entry/src/main/ets/view/ItemDescView/DescTravelImageView.ets
+++ b/entry/src/main/ets/view/ItemDescView/DescTravelImageView.ets
@@ -19,7 +19,7 @@
 
 @Component
 export struct DescTravelImageView {
-  @Prop item: ViewItem = new ViewItem();
+  @ObjectLink item: ViewItem;
   private numberFormat: intl.NumberFormat = new intl.NumberFormat('collectionsCount', { maximumFractionDigits: 1 });
   @Prop @Watch('onIsLikeChange') isLike: boolean = false;
   @State flag: boolean = false;


```

## [47/50] ID: OH_0152 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-object-link-to-replace-prop`
- **Result:** `PASS`
- **Target File:** `CertManager/src/main/ets/pages/picker/AuthorizedAppManagementPage.ets`
- **Warning:** Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

###  Buggy Snippet
```typescript
@Component
export struct AuthorizedAppManagementPage {
  private stack?: NavPathStack;

  @State presenter: CmShowAppCredPresenter = CmShowAppCredPresenter.getInstance();
  @Prop sheetParam: SheetParam;
  @State private headRectHeight: number = 64;
  @State private headRectHeightReal: number = 0;
  private scroller: Scroller = new Scroller();
  @State private scrollerHeight: number = 0;

  build() {
    NavDestination() {
      Stack({ alignContent: Alignment.Top }) {
        Column() {
          HeadComponent({ headName: $r('app.string.managerAuthApp'), isStartBySheet: true, onBackClicked: () => {
            this.stack?.pop();
          } })
            .margin({
              left: $r('app.float.wh_value_12'),
              top: 8
            })
        }.zIndex(1)
        .onAreaChange((oldArea, newArea) => {
          this.headRectHeight = newArea.height as number;
          this.headRectHeightReal = newArea.height as number;
        })

        Stack({ alignContent: Alignment.TopEnd }) {
          Scroll(this.scroller) {
            List() {
              ForEach(this.presenter.appInfoList, (item: AppAuthorVo, index) => {
                ListItem() {
                  DialogComponent({ appImage: item.appImage, appName: item.appName,
                    indexNum: index, uidItem: $presenter,
                    onChanged: async () => {
                      await this.presenter.removeGrantedAppList(this.presenter.credInfo.keyUri);
                      this.presenter.getAuthorizedAppList(this.presenter.credInfo.keyUri);
                    } })
                }
              })
            }
            .scrollBar(BarState.Off)
            .divider({
              strokeWidth: $r('app.float.Evidence_strokeWidth'),
              color: $r('sys.color.ohos_id_color_list_separator'),
              startMargin: 64
            })
          }
          .align(Alignment.Top)
          .edgeEffect(EdgeEffect.Spring)
          .constraintSize({
            minHeight: this.getScrollMinHeight()
          })
          .scrollBar(BarState.Off)
          .padding({
            left: $r('app.float.wh_value_24'),
            bottom: $r('app.float.wh_value_24')
          }).onAreaChange((oldArea, newArea) => {
            this.scrollerHeight = newArea.height as number;
          })

          Column() {
            ScrollBar({
              scroller: this.scroller,
              direction: ScrollBarDirection.Vertical,
              state: BarState.Auto
            }).margin({
              bottom: $r('app.float.wh_value_24')
            })
          }.height(this.scrollerHeight)
        }.padding({
          top: this.headRectHeight
        })
      }
    }
    .hideTitleBar(true)
    .width(WidthPercent.WH_100_100)
    .height(this.sheetParam?.lastSheetPage === NavEntryKey.AUTHORIZED_APP_ENTRY ? WidthPercent.WH_AUTO : this.sheetParam?.sheetMinHeight)
    .backgroundColor($r('sys.color.background_secondary'))
    .onReady((ctx: NavDestinationContext) => {
      this.stack = ctx.pathStack;
      try {
        this.presenter = (ctx.pathInfo.param as AuthorizedAppManagementParam).presenter;
      } catch (err) {
        let error = err as BusinessError;
        console.error(TAG + 'Get presenter failed: ' + error?.code + ', message: ' + error?.message);
      }
    })
  }

  getScrollMinHeight() {
    if (this.sheetParam === undefined || this.headRectHeightReal === 0 ||
      this.sheetParam.sheetMinHeight < this.headRectHeightReal) {
      return 0;
    }
    return this.sheetParam.sheetMinHeight - this.headRectHeightReal;
  }
}
```

### Patch
```diff
// File: CertManager/src/main/ets/pages/picker/AuthorizedAppManagementPage.ets
--- a/CertManager/src/main/ets/pages/picker/AuthorizedAppManagementPage.ets
+++ b/CertManager/src/main/ets/pages/picker/AuthorizedAppManagementPage.ets
@@ -37,7 +37,7 @@
   private stack?: NavPathStack;
 
   @State presenter: CmShowAppCredPresenter = CmShowAppCredPresenter.getInstance();
-  @Prop sheetParam: SheetParam;
+  @ObjectLink sheetParam: SheetParam;
   @State private headRectHeight: number = 64;
   @State private headRectHeightReal: number = 0;
   private scroller: Scroller = new Scroller();


```

## [48/50] ID: OH_0044 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- **Result:** `PASS`
- **Target File:** `entry/src/main/ets/pages/favorites/editFavoriteList.ets`
- **Warning:** Do not use stringify in the key generator function of LazyForEach

###  Buggy Snippet
```typescript
@Component
struct FavoriteContent {
  @Link presenter: EditFavoriteListPresenter;
  isUsuallyShow: boolean = false;
  @Link selectNumbers: number;
  @Link favoriteNumber: number;
  @Link usuallyNumber: number;
  @State selectNumber: number = this.selectNumbers;
  @State selectFavoriteIdList: string[] = [];
  @State isEditSelectList: string[] = null != this.presenter.isEditSelect &&
    this.presenter.isEditSelect.length > 0 ? this.presenter.isEditSelect : [];
  @State favoriteListPresenter: EditFavoriteListPresenter = this.presenter;
  @State isSelectAll: boolean = false;
  @State isSelectAllStatus: boolean = false;
  item: FavoriteListBean = new FavoriteListBean(0,false,false,new FavoriteBean('',0,'','','','','',false,'',false,0,''),
    new SearchContactsBean('','','','','','','','','',0,'','','','','',''));
  @State text: string = '';
  @State isEditDrag: boolean = false;
  @State select: number = 0;
  @State currentIndex: number = 0;
  @State isDragShow: boolean = false;
  @State offsetY: number = 50;
  @State positionYDown: number = 0;
  @State positionYUp: number = 0;

  @Builder pixelMapBuilder() {
    Column() {
      FavoriteListItem({
        item: this.item,
        isEditSelectList: $isEditSelectList,
        presenter: $favoriteListPresenter,
        selectNumber: $selectNumber,
        isSelectAll: $isSelectAll,
        usuallyNumber: $usuallyNumber,
        favoriteNumber: $favoriteNumber,
        isEditDrag: this.isEditDrag
      })
    }
  }

  build() {
    Stack({ alignContent: Alignment.BottomEnd }) {
      Column() {
        Stack({ alignContent: Alignment.TopStart }) {
          Row() {
            Text(this.selectNumber > 0 ? $r('app.string.select_num', this.selectNumber) : $r('app.string.no_select'))
              .maxFontSize(22)
              .minFontSize(18)
              .maxLines(1)
              .fontWeight(FontWeight.Bold)
              .fontColor(Color.Black)
              .margin({ top: $r('app.float.id_card_margin_large'), bottom: $r('app.float.id_card_margin_large') })
          }
          .margin({ left: this.offsetY < 0 ? 0 : $r('app.float.id_item_height_mid') })
          .height(this.offsetY > 0 ? 56 : 138)
          .animation({
            duration: 200,
            iterations: 1,
          })

          TitleGuide({
            isDragShow: $isDragShow,
            isEditSelectList: $isEditSelectList,
            presenter: $favoriteListPresenter,
            selectNumber: $selectNumber,
            offsetY: $offsetY
          })
        }

        GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
          GridCol({ span: { sm: 4, md: 6, lg: 8 }, offset: { sm: 0, md: 1, lg: 2 } }) {
            List({ space: 0, initialIndex: 0 }) {
              LazyForEach(this.presenter.favoriteDataSource, (item: FavoriteListBean, index: number) => {
                ListItem() {
                  FavoriteListItem({
                    item: item,
                    isEditSelectList: $isEditSelectList,
                    presenter: $favoriteListPresenter,
                    selectNumber: $selectNumber,
                    isSelectAll: $isSelectAll,
                    usuallyNumber: $usuallyNumber,
                    favoriteNumber: $favoriteNumber,
                    isEditDrag: false
                  })
                }
                .onDragStart((event: DragEvent, extraParams: string) => {
                  console.log('ListItem onDragStarts, ' + extraParams)
                  let jsonString: Extra = JSON.parse(extraParams)
                  if (jsonString.selectedIndex >= this.favoriteNumber) {
                    console.log('List onDragStarts , return ')
                    return;
                  }
                  this.isEditDrag = true;
                  this.select = jsonString.selectedIndex;
                  this.item = item;
                  return this.pixelMapBuilder();
                })
              }, (item:FavoriteListBean) => JSON.stringify(item))
            }
            .editMode(true)
            .width('100%')
            .height('100%')
            .scrollBar(BarState.Off)
            .listDirection(Axis.Vertical)
            .edgeEffect(EdgeEffect.Spring)
            .onDrop((event: DragEvent, extraParams: string) => {
              let jsonString = JSON.parse(extraParams) as extraParamsObj;
              if (jsonString.insertIndex >= this.favoriteNumber) {
                return;
              }
              if (this.isEditDrag) {
                this.isDragShow = true;
                let index = this.presenter.favoriteDataSource.getFavoriteList().indexOf(this.item.favorite);
                this.presenter.favoriteDataSource.getFavoriteList().splice(index, 1);
                this.presenter.favoriteDataSource.getFavoriteList()
                  .splice(jsonString.insertIndex, 0, this.item.favorite);
                this.presenter.favoriteDataSource.refresh(this.presenter.favoriteDataSource.getFavoriteList());
                this.isEditDrag = false;
              }
            })
            .onScroll((scrollOffset, scrollState) => {
              this.offsetY = this.positionYDown - this.positionYUp;
              if (this.offsetY > 0) {
                animateTo({ duration: 1000 }, () => {
                });
              } else {
                animateTo({ duration: 1000 }, () => {
                });
              }
            })
            .onTouch((event) => {
              switch (event.type) {
                case TouchType.Down:
                  this.positionYDown = Math.abs(event.touches[0].y);
                  break;
                case TouchType.Move:
                  this.positionYUp = Math.abs(event.touches[0].y);
                case TouchType.Up:
                  this.positionYUp = Math.abs(event.touches[0].y);
                  break;
              }
            })
          }
        }
        .height('100%')
        .flexShrink(1)

        Row() {
          Flex({ direction: FlexDirection.Row, justifyContent: FlexAlign.SpaceBetween }) {
            Column() {
              Image(this.selectNumber > 0 ? $r('app.media.ic_public_close') : $r('app.media.ic_public_close_gray'))
                .objectFit(ImageFit.Contain)
                .height($r('app.float.id_card_image_small'))
                .width($r('app.float.id_card_image_small'))
                .margin({ bottom: 3 })
              Text($r('app.string.favorite_remove'))
                .fontColor(this.selectNumber > 0 ? $r('sys.color.ohos_id_color_toolbar_text') : Color.Gray)
                .fontSize($r('sys.float.ohos_id_text_size_caption'))
                .fontWeight(FontWeight.Medium)
                .margin({ top: $r('app.float.id_card_margin_large') })
            }
            .onClick(() => {
              if (this.isEditSelectList.length > 0) {
                this.presenter.deleteFavoriteInfo(this.isEditSelectList);
                this.isEditSelectList = [];
                this.selectNumber = this.isEditSelectList.length;
                router.back();
              }
            })
            .width('40%')
            .height('100%')
            .alignItems(HorizontalAlign.Center)
            .justifyContent(FlexAlign.Center)

            Column() {
              Image(this.presenter.favoriteList.length === this.selectNumber ? $r('app.media.ic_public_select_all_filled') : $r('app.media.ic_public_select_all'))
                .objectFit(ImageFit.Contain)
                .height($r('app.float.id_card_image_small'))
                .width($r('app.float.id_card_image_small'))
                .margin({ bottom: 3 })
                .fillColor($r('sys.color.ohos_id_color_primary'))
              Text(this.presenter.favoriteList.length === this.selectNumber ? $r('app.string.unselect_all') : $r('app.string.select_all'))
                .fontColor(this.presenter.favoriteList.length === this.selectNumber ? $r('sys.color.ohos_id_color_toolbar_text') : Color.Gray)
                .fontSize($r('sys.float.ohos_id_text_size_caption'))
                .fontWeight(FontWeight.Medium)
                .margin({ top: $r('app.float.id_card_margin_large') })

            }
            .onClick(() => {
              this.isSelectAll = this.presenter.favoriteList.length === this.selectNumber;
              if (this.isSelectAll) {
                this.isEditSelectList = this.presenter.cancelAllFavoriteSelectInfo(this.presenter.favoriteList, this.isEditSelectList);
              } else {
                this.isEditSelectList = this.presenter.addAllFavoriteSelectInfo(this.presenter.favoriteList);
              }
              this.selectNumber = this.isEditSelectList.length;
              this.presenter.favoriteDataSource.refresh(this.presenter.favoriteList);
            })
            .width('40%')
            .height('100%')
            .alignItems(HorizontalAlign.Center)
            .justifyContent(FlexAlign.Center)
          }
        }
        .padding({ left: 24, right: 24 })
        .backgroundColor(Color.White)
        .width('100%')
        .height($r('app.float.id_item_height_max'))
      }
      .padding({ left: 24, right: 24 })
      .height('100%')
      .width('100%')
    }
    .height('100%')
    .width('100%')
  }
}
```

### Patch
```diff
// File: entry/src/main/ets/pages/favorites/editFavoriteList.ets
--- a/entry/src/main/ets/pages/favorites/editFavoriteList.ets
+++ b/entry/src/main/ets/pages/favorites/editFavoriteList.ets
@@ -193,7 +193,7 @@
                   this.item = item;
                   return this.pixelMapBuilder();
                 })
-              }, (item:FavoriteListBean) => JSON.stringify(item))
+              }, (item:FavoriteListBean) => item.favorite.contactId + '_' + item.index)
             }
             .editMode(true)
             .width('100%')


```

## [49/50] ID: OH_0144 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-suggest-use-effectkit-blur`
- **Result:** `PASS`
- **Target File:** `product/phone/dropdownpanel/src/main/ets/pages/index.ets`
- **Warning:** Suggestion Use effectKit.createEffect to create a blur effect

###  Buggy Snippet
```typescript
@Component
struct Index {
  @State showComponentName: DropdownPanelComponentName = DropdownPanelComponentName.NONE;
  @State componentOptAreaHeightPX: number = 0;
  @StorageLink('StatusCoefficient') StatusCoefficient: number = 1.0;
  mCallback: any;
  mClearCallbacks: unsubscribe[];
  settingDataKey = 'settings.display.navigationbar_status';
  urivar: string = null;
  helper: dataShare.DataShareHelper = null;
  mNavigationBarStatusDefaultValue: string = '1';
  navigationBarWidth: number = 0;
  mNeedUpdate: boolean = false;
  mWidthPx: number = 0;
  @State mNotificationInsert: insertTemplate = new insertTemplate();
  @State mNotificationDelete: insertTemplate = new insertTemplate();
  @State mControlCenterInsert: insertTemplate = new insertTemplate();
  @State mControlCenterDelete: insertTemplate = new insertTemplate();
  @State componentOptAreaTranslateY: string = '0px';
  @State backgroundOpacity: number = 0;

  onBackPress(): boolean {
    return true
  }

  aboutToAppear() {
    Log.showInfo(TAG, `aboutToAppear, start`);

    setAppBgColor('#00000000');
    CommonStyleManager.setAbilityPageName(TAG);
    StyleManager.setStyle();

    let dropdownRect = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_DROPDOWN_PANEL, 'rect');
    let navigationBarRect = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_NAVIGATION_BAR, 'config');
    this.initHelper(dropdownRect, navigationBarRect);
    this.resizeDropdownPanelAndNavigationBar(dropdownRect, navigationBarRect);
    Log.showDebug(TAG, `getValueSync componentOptAreaHeightPX: ${this.componentOptAreaHeightPX}`);

    this.componentOptAreaTranslateY = (-this.componentOptAreaHeightPX * 0.1) + 'px';

    this.mClearCallbacks = [];
    this.mClearCallbacks.push(
    EventManager.subscribe('DropdownEvent', (args) => this.onDropdownEvent(args)),
    EventManager.subscribe(START_ABILITY_EVENT, (args) => this.onStartAbility(args)),
    EventManager.subscribe('hideNotificationWindowEvent', (args) => this.onHideNotificationWindowEvent(args)));

    mHeightConfigUtils = new HeightConfigUtils();
    let StatusCoefficient;

    StatusCoefficient = AppStorage.SetAndLink("StatusCoefficient", 1.0);
    StatusCoefficient.set(mHeightConfigUtils.getStatusCoefficient());

    let signalObserved = AppStorage.SetAndLink("signalObserved", false);
    signalObserved.set(false);

    this.mCallback = {
      "onStateChange": (data) => this.onStateChange(data),
      "onNotificationShowOrHide": (data) => this.onNotificationShowOrHide(data),
      "onControlShowOrHide": (data) => this.onControlShowOrHide(data)
    };
    NavigationEvent.registerCallback(this.mCallback);
    MultimodalInputManager.registerControlListener(this.mCallback);
    MultimodalInputManager.registerNotificationListener(this.mCallback);
    Log.showDebug(TAG, `aboutToAppear, end`);
  }

  private async initHelper(dropdownRect, navigationBarRect): Promise<void> {
    this.urivar = Constants.getUriSync(Constants.KEY_NAVIGATIONBAR_STATUS);
    this.helper = await dataShare.createDataShareHelper(AbilityManager.getContext(AbilityManager.ABILITY_NAME_DROPDOWN_PANEL), this.urivar);
    Log.showDebug(TAG, `initHelper ${this.helper}, uri: ${JSON.stringify(this.urivar)}`);
    this.helper?.on("dataChange", this.urivar, () => {
      this.resizeDropdownPanelAndNavigationBar(dropdownRect, navigationBarRect);
      Log.showInfo(TAG, `NavigationBar status change, componentOptAreaHeightPX: ${this.componentOptAreaHeightPX}`);
    });
  }

  onPageShow() {
    Log.showInfo(TAG, `onPageShow, start`)
    if (this.showComponentName === DropdownPanelComponentName.NONE) {
      return
    }
    StatusBarVM.setUseInWindowName(WindowType.DROPDOWN_PANEL)
    Trace.end(Trace.CORE_METHOD_START_DROPDOWNPANEL)
  }

  aboutToDisappear() {
    Log.showInfo(TAG, `aboutToDisappear`)
    this.mClearCallbacks.forEach((mClearCallback: Function) => {
      mClearCallback()
      mClearCallback = undefined
    })
    this.mClearCallbacks = undefined
  }

  resizeDropdownPanelAndNavigationBar(dropdownRect, navigationBarRect) {
    Log.showDebug(TAG, `resizeDropdownPanelAndNavigationBar, dropdownRect: ${JSON.stringify(dropdownRect)} navigationBarRect: ${JSON.stringify(navigationBarRect)}`)
    let context = AbilityManager.getContext(AbilityManager.ABILITY_NAME_DROPDOWN_PANEL);
    this.mNavigationBarStatusDefaultValue = settings.getValueSync(context, this.settingDataKey, '1');
    this.componentOptAreaHeightPX = this.mNavigationBarStatusDefaultValue == '1' ? dropdownRect.height - navigationBarRect.realHeight : dropdownRect.height;
    this.navigationBarWidth = this.mNavigationBarStatusDefaultValue == '1' ? navigationBarRect.height : 0;
    WindowManager.resetSizeWindow(WindowType.NAVIGATION_BAR, { ...navigationBarRect, height: this.navigationBarWidth })
    WindowManager.resetSizeWindow(WindowType.DROPDOWN_PANEL, { ...dropdownRect, height: this.componentOptAreaHeightPX })
  }

  onNotificationShowOrHide(data) {
    Log.showDebug(TAG, `mNotificationAsyncCallback preKeys: ${data.preKeys}, finalKey: ${data.finalKey}`);
    Log.showDebug(TAG, `this.showComponentName: ${this.showComponentName}`);
    if (this.showComponentName === DropdownPanelComponentName.NOTIFICATION) {
      this.hideSelf();
    } else {
      this.showSelf('Notification');
    }
    Log.showDebug(TAG, `mNotificationAsyncCallback end`);
  }

  onControlShowOrHide(data) {
    Log.showDebug(TAG, `mControlAsyncCallback preKeys: ${data.preKeys}, finalKey: ${data.finalKey}`);
    Log.showDebug(TAG, `this.showComponentName: ${this.showComponentName}`);
    if (this.showComponentName === DropdownPanelComponentName.CONTROL_CENTER) {
      this.hideSelf();
    } else {
      this.showSelf('ControlCenter');
    }
    Log.showDebug(TAG, `mControlAsyncCallback end`);
  }

  onStateChange(data) {
    Log.showDebug(TAG, `onStateChange, data: ${JSON.stringify(data)}`)
    Log.showDebug(TAG, `onStateChange, showComponentName: ${this.showComponentName}`)
    if (this.showComponentName !== DropdownPanelComponentName.NONE) {
      this.hideSelf()
    }
  }

  onDropdownEvent(args) {
    Log.showDebug(TAG, `onDropdownEvent, args: ${JSON.stringify(args)}`)
    this.showSelf(args.dropdownArea == 'left' ? 'Notification' : 'ControlCenter')
  }

  onStartAbility(args) {
    Log.showDebug(TAG, `onStartAbility, args: ${args}`)
    this.hideSelf()
  }

  onHideNotificationWindowEvent(args) {
    Log.showDebug(TAG, `onHideNotificationWindowEvent, args: ${args}`)
    this.hideSelf()
  }

  onTouchMove(data) {
    Log.showDebug(TAG, `onTouchMove, data: ${JSON.stringify(data)}`)
    if (data.direction == 'top') {
      this.hideSelf()
    } else if (data.direction == 'left' && data.touchComponent == 'notification') {
      this.switchNotificationOrControlCenter('ControlCenter')
    } else if (data.direction == 'right' && data.touchComponent == 'control') {
      this.switchNotificationOrControlCenter('Notification')
    } else if (data.direction == 'drop_left' && data.touchComponent == 'control') {
      this.showComponentName = DropdownPanelComponentName.NOTIFICATION
    } else if (data.direction == 'drop_right' && data.touchComponent == 'notification') {
      this.showComponentName = DropdownPanelComponentName.CONTROL_CENTER
    }
  }

  switchNotificationOrControlCenter(showComponentName) {
    Log.showDebug(TAG, `switchNotificationOrControlCenter, showComponentName: ${showComponentName}`)
    this.mNotificationInsert = { type: TransitionType.Insert, opacity: 0, translate: { x: (-this.mWidthPx) + 'px' } }
    this.mControlCenterInsert = { type: TransitionType.Insert, opacity: 0, translate: { x: (this.mWidthPx) + 'px' } }
    let transitionDelete = {
      type: TransitionType.Delete,
      opacity: 0,
      scale: { x: 0.8, y: 0.8, centerX: '50%', centerY: '50%' }
    }
    this.mNotificationDelete = transitionDelete
    this.mControlCenterDelete = transitionDelete
    this._animateTo({ ...SHOW_ANIM_CONFIG, onFinish: () => {
      Log.showInfo(TAG, `switchNotificationOrControlCenter, show anim finish.`);
    } }, () => {
      this.showComponentName = showComponentName
    })
  }

  showSelf(showComponentName) {
    Log.showDebug(TAG, `showSelf, showComponentName: ${showComponentName}`)
    this.showComponentName = showComponentName
    WindowManager.showWindow(WindowType.DROPDOWN_PANEL)
    this.componentOptAreaTranslateY = '0px'
    this.backgroundOpacity = 1
    Trace.start(Trace.CORE_METHOD_START_DROPDOWNPANEL)
  }

  hideSelf() {
    Log.showDebug(TAG, `hideSelf`)
    this._animateTo({...SHOW_ANIM_CONFIG, onFinish: () => {
      Log.showInfo(TAG, `hideSelf, hide anim finish.`);
      WindowManager.hideWindow(WindowType.DROPDOWN_PANEL)
    }}, () => {
      this.componentOptAreaTranslateY = (-this.componentOptAreaHeightPX * 0.1) + 'px'
      this.backgroundOpacity = 0
      this.showComponentName = DropdownPanelComponentName.NONE
    })
  }

  _animateTo(config, callback) {
    Log.showDebug(TAG, `_animateTo, config: ${JSON.stringify(config)}`)
    animateTo(config, callback)
    setTimeout(config.onFinish, config.duration + config.delay)
  }

  build() {
    Stack({ alignContent: Alignment.Top }) {
      Image($r("app.media.dropdownpanel_bgc"))
        .width('100%')
        .height('100%')
        .objectFit(ImageFit.Fill)
        .blur(25)
        .opacity(1)
      Column() {
        if (this.showComponentName === DropdownPanelComponentName.NOTIFICATION) {
          Notification({ touchMoveCallback: (data) => this.onTouchMove(data) })
            .transition(this.mNotificationInsert)
            .transition(this.mNotificationDelete)
        }
        if (this.showComponentName === DropdownPanelComponentName.CONTROL_CENTER) {
          ControlCenterComponent({
            touchMoveCallback: (data) => this.onTouchMove(data)
          })
            .transition(this.mControlCenterInsert)
            .transition(this.mControlCenterDelete)
        }
      }
      .width('100%')
      .height(this.componentOptAreaHeightPX + 'px')
      .translate({ y: this.componentOptAreaTranslateY })
    }
    .width('100%')
    .height('100%')
    .backgroundColor($r("app.color.default_background"))
    .opacity(1)
    .onAreaChange((e, e2) => {
      Log.showInfo(TAG, `onAreaChange, e: ${JSON.stringify(e)} e2: ${JSON.stringify(e2)}`);
      this.mWidthPx = vp2px(Number(e2.width))
    })
  }
}
```

### Patch
```diff
// File: product/phone/dropdownpanel/src/main/ets/pages/index.ets
--- a/product/phone/dropdownpanel/src/main/ets/pages/index.ets
+++ b/product/phone/dropdownpanel/src/main/ets/pages/index.ets
@@ -24,6 +24,7 @@
 
 import AbilityManager from '../../../../../../../common/src/main/ets/default/abilitymanager/abilityManager';
 import image from "@ohos.multimedia.image"
+import effectKit from '@ohos.effectKit'
 import Log from '../../../../../../../common/src/main/ets/default/Log'
 import Trace from '../../../../../../../common/src/main/ets/default/Trace'
 import WindowManager, { WindowType, WINDOW_SHOW_HIDE_EVENT
@@ -97,9 +98,24 @@
   @State mControlCenterDelete: insertTemplate = new insertTemplate();
   @State componentOptAreaTranslateY: string = '0px';
   @State backgroundOpacity: number = 0;
+  @State blurredPixelMap: image.PixelMap = undefined;
 
   onBackPress(): boolean {
     return true
+  }
+
+  async createBlurEffect() {
+    try {
+      const resourceMgr = getContext(this).resourceManager;
+      const fileData = await resourceMgr.getMediaContent($r("app.media.dropdownpanel_bgc").id);
+      const imageSource = image.createImageSource(fileData.buffer);
+      const pixelMap = await imageSource.createPixelMap();
+      const effectFilter = effectKit.createEffect(pixelMap);
+      effectFilter.blur(25);
+      this.blurredPixelMap = await effectFilter.getPixelMap();
+    } catch (err) {
+      Log.showError(TAG, `createBlurEffect error: ${JSON.stringify(err)}`);
+    }
   }
 
   aboutToAppear() {
@@ -108,6 +124,8 @@
     setAppBgColor('#00000000');
     CommonStyleManager.setAbilityPageName(TAG);
     StyleManager.setStyle();
+
+    this.createBlurEffect();
 
     let dropdownRect = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_DROPDOWN_PANEL, 'rect');
     let navigationBarRect = AbilityManager.getAbilityData(AbilityManager.ABILITY_NAME_NAVIGATION_BAR, 'config');
@@ -288,11 +306,10 @@
 
   build() {
     Stack({ alignContent: Alignment.Top }) {
-      Image($r("app.media.dropdownpanel_bgc"))
+      Image(this.blurredPixelMap ? this.blurredPixelMap : $r("app.media.dropdownpanel_bgc"))
         .width('100%')
         .height('100%')
         .objectFit(ImageFit.Fill)
-        .blur(25)
         .opacity(1)
       Column() {
         if (this.showComponentName === DropdownPanelComponentName.NOTIFICATION) {


```

## [50/50] ID: OH_0141 | ArkTS (T)
- **Rule ID:** `@performance/hp-arkui-use-transition-to-replace-animateto`
- **Result:** `PASS`
- **Target File:** `product/pc/notificationpanel/src/main/ets/pages/index.ets`
- **Warning:** Use transition for component transition animation

###  Buggy Snippet
```typescript
@Component
struct Index {
  @State mOpacity: number = 0.0;
  @State mWidthSize: number = 0.2
  @State mHeightSize: number = 0.2
  @State mBackground: PixelMap | undefined = undefined;
  mClearCallbacks: Array<unsubscribe> = [];
  mShowAnimReady: boolean = false;

  aboutToAppear() {
    Log.showInfo(TAG, `aboutToAppear, start`)
    setAppBgColor('#00000000')
    this.initWindowPolicy();
  }

  onPageShow() {
    Log.showInfo(TAG, `onPageShow`)
    this.showAnimation();
  }

  onPageHide() {
    Log.showInfo(TAG, `onPageHide`)
  }

  aboutToDisappear() {
    Log.showInfo(TAG, `aboutToDisappear`)
    this.mClearCallbacks.forEach((unsubscribe) => unsubscribe());
    this.mClearCallbacks.length = 0;
  }

  build() {
    Column(){
      Stack() {
        Image(this.mBackground)
          .width('100%')
          .height('100%')
          .objectFit(ImageFit.Fill)
        Column() {
          Notification()
        }
        .backgroundColor($r('app.color.default_background'))
        .width('100%')
        .height('100%')
      }
      .width('97%')
      .height('97%')
      .clip(true)
      .opacity(this.mOpacity)
      .borderRadius($r('app.float.default_border_radius'))
      .scale({
        x: this.mWidthSize,
        y: this.mHeightSize,
        z: 1,
        centerX: '100%',
        centerY: '0%'
      })
    }
    .width('100%')
    .height('100%')
    .alignItems(HorizontalAlign.End)
  }

  initWindowPolicy() {
    Log.showDebug(TAG, `init notification panel window Policy`);
    this.mClearCallbacks.push(
    EventManager.subscribe(SHOW_EVENT, () => WindowManager.showWindow(WindowType.NOTIFICATION_PANEL)),
    EventManager.subscribe(HIDE_EVENT, () => this.hideWindow()),
    EventManager.subscribe(START_ABILITY_EVENT, () => this.hideWindow()),
    EventManager.subscribe(WINDOW_SHOW_HIDE_EVENT, (args) => {
      let { windowName, isShow } = args;
      Log.showInfo(TAG, `WINDOW_SHOW_HIDE_EVENT windowName: ${windowName}, isShow: ${isShow}`);
      windowName == WindowType.CONTROL_PANEL && isShow && this.hideWindow();
      windowName == WindowType.NOTIFICATION_PANEL && isShow && (this.mShowAnimReady = true);
    }),
    EventManager.subscribe('NotificationWindowResizeEvent',async (args) => {
      let { windowName, rect } = args;
      let dis = await display.getDefaultDisplay();
      Log.showInfo(TAG, `NotificationWindowResizeEvent: ${windowName}, isShow: ${rect}`);
      AbilityManager.setAbilityData(AbilityManager.ABILITY_NAME_NOTIFICATION_PANEL, 'rect', rect);
      AbilityManager.setAbilityData(AbilityManager.ABILITY_NAME_NOTIFICATION_PANEL, 'dis', {
        width: dis.width,
        height: dis.height,
      });
      WindowManager.resetSizeWindow(windowName, rect).then(
      ).then(() => {
      }).catch((err) => {
      });
    }),
    MultimodalInputManager.subscribeCombinationKey([MultiKeyCode.WIN, MultiKeyCode.N], (data) => {
      let windowInfo = WindowManager.getWindowInfo(WindowType.NOTIFICATION_PANEL);
      Log.showInfo(TAG, `on CombinationKeyEvent: data: ${data}, windowInfo: ${windowInfo?.visibility}`);
      if (windowInfo) {
          windowInfo.visibility
          ? this.hideWindow()
          : WindowManager.showWindow(WindowType.NOTIFICATION_PANEL);
      }
    })
    );
  }

  _animateTo(config, callback) {
    animateTo(config, callback)
    setTimeout(config.onFinish, config.duration + config.delay)
  }

  showAnimation(){

    //init page state
    this.mOpacity = 0;
    this.mWidthSize = 0.7;
    this.mHeightSize = 0.7;

    //show animation
    animateTo({
      duration: 200,
      curve: Curve.Friction
    }, () => {
      this.mOpacity = 1;
      this.mWidthSize = 1.03;
      this.mHeightSize = 1.03;
    })
    animateTo({
      duration:100,
      curve: Curve.Friction,
      delay: 200
    }, () =>{
      this.mWidthSize = 1;
      this.mHeightSize = 1;
    })
  }

  hideAnimation(){
    //hide animation
    animateTo({
      duration: 100,
      curve: Curve.Friction,
      onFinish: () => {
        WindowManager.hideWindow(WindowType.NOTIFICATION_PANEL);
      }
    }, () => {
      this.mWidthSize = 0.7;
      this.mHeightSize = 0.7;
      this.mOpacity = 0;
    })
  }

  hideWindow() {
    Log.showInfo(TAG, `do hide window.`);
    this.hideAnimation();
  }
}
```

### Patch
```diff
// File: product/pc/notificationpanel/src/main/ets/pages/index.ets
--- a/product/pc/notificationpanel/src/main/ets/pages/index.ets
+++ b/product/pc/notificationpanel/src/main/ets/pages/index.ets
@@ -39,6 +39,7 @@
   @State mWidthSize: number = 0.2
   @State mHeightSize: number = 0.2
   @State mBackground: PixelMap | undefined = undefined;
+  @State mIsVisible: boolean = false;
   mClearCallbacks: Array<unsubscribe> = [];
   mShowAnimReady: boolean = false;
 
@@ -89,6 +90,9 @@
         centerX: '100%',
         centerY: '0%'
       })
+      .transition(TransitionEffect.OPACITY.animation({ duration: 200, curve: Curve.Friction })
+        .combine(TransitionEffect.scale({ x: 0.7, y: 0.7, z: 1, centerX: '100%', centerY: '0%' })
+          .animation({ duration: 200, curve: Curve.Friction })))
     }
     .width('100%')
     .height('100%')
@@ -133,50 +137,34 @@
     );
   }
 
-  _animateTo(config, callback) {
-    animateTo(config, callback)
-    setTimeout(config.onFinish, config.duration + config.delay)
-  }
-
   showAnimation(){
-
     //init page state
     this.mOpacity = 0;
     this.mWidthSize = 0.7;
     this.mHeightSize = 0.7;
 
-    //show animation
-    animateTo({
-      duration: 200,
-      curve: Curve.Friction
-    }, () => {
+    //show animation - using state changes with transition
+    setTimeout(() => {
       this.mOpacity = 1;
       this.mWidthSize = 1.03;
       this.mHeightSize = 1.03;
-    })
-    animateTo({
-      duration:100,
-      curve: Curve.Friction,
-      delay: 200
-    }, () =>{
+    }, 0);
+    
+    setTimeout(() => {
       this.mWidthSize = 1;
       this.mHeightSize = 1;
-    })
+    }, 200);
   }
 
   hideAnimation(){
-    //hide animation
-    animateTo({
-      duration: 100,
-      curve: Curve.Friction,
-      onFinish: () => {
-        WindowManager.hideWindow(WindowType.NOTIFICATION_PANEL);
-      }
-    }, () => {
-      this.mWidthSize = 0.7;
-      this.mHeightSize = 0.7;
-      this.mOpacity = 0;
-    })
+    //hide animation - using state changes with transition
+    this.mWidthSize = 0.7;
+    this.mHeightSize = 0.7;
+    this.mOpacity = 0;
+    
+    setTimeout(() => {
+      WindowManager.hideWindow(WindowType.NOTIFICATION_PANEL);
+    }, 100);
   }
 
   hideWindow() {


```
