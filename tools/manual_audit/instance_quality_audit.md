# Instance Quality Audit

This document contains 100 randomly sampled instances (50 ArkTS, 50 C/C++) to verify that each describes a genuine, repairable defect.

## [1/100] ID: OH_0328 | ArkTS (T)
- Rule ID: `@hw-stylistic/operator-linebreak`
- Target File: `HMRouterTransitions/src/main/ets/longTake/LongTakeSession.ets`
- Warning: '-' should be placed at the end of the line.

### Buggy Snippet
```typescript
{
      if (initScaleX >= initScaleY) {
        this.initScale = initScaleX;
        this.initTranslateX = px2vp(cardItemInfo_px.left);
        this.initClipWidth = px2vp(stackSize_px?.width);
        this.initClipHeight = px2vp((cardItemInfo_px.height) / this.initScale);
        this.snapShotSize = { width: px2vp(stackSize_px?.width) };
        this.initTranslateY = px2vp(cardItemInfo_px.top);
      } else {
        this.initScale = initScaleY;
        this.initTranslateY = px2vp(cardItemInfo_px.top);
        this.initClipHeight = px2vp(stackSize_px?.height);
        this.initClipWidth = px2vp((cardItemInfo_px.width) / this.initScale);
        this.initTranslateX = px2vp(cardItemInfo_px.left);
        this.snapShotSize = { height: px2vp(stackSize_px?.height) };
      }
    } else {
      let postNodePositionX_vp = postNode.getPositionToWindowWithTransform().x;
      let postNodePositionY_vp = postNode.getPositionToWindowWithTransform().y;
      let postNodeWidth_px = postNode.getMeasuredSize().width;
      let postNodeHeight_px = postNode.getMeasuredSize().height;


      this.initPositionValueX = -postNodePositionX_vp + snapShotStackPositionToWindow_vp?.x!;
      this.initPositionValueY = -postNodePositionY_vp + snapShotStackPositionToWindow_vp?.y!;
      this.snapShotPositionY = postNodePositionY_vp - snapShotStackPositionToWindow_vp?.y!
        - ((stackPosition_vp?.y!) != 0 ? 0 :
          (isWindowLayoutFullScreen ? 0 : px2vp(WindowUtils.topAvoidAreaHeight_px)));
      this.snapShotPositionX = postNodePositionX_vp - snapShotStackPositionToWindow_vp?.x!;

      this.initScale = cardItemInfo_px.width / postNodeWidth_px;

      let inspectorInfo = sourceNode?.getInspectorInfo();
      this.initBorderRadius = inspectorInfo ? (inspectorInfo as ESObject).$attrs.borderRadius : 0;

      if (typeof this.initBorderRadius === 'string') {
        this.initBorderRadius = parseFloat(this.initBorderRadius) / this.initScale
      }

      this.initClipHeight = px2vp(cardItemInfo_px.height / this.initScale);
      this.initTranslateY = px2vp(cardItemInfo_px.top);
      this.initClipWidth = px2vp(postNodeWidth_px);
      this.snapShotSize = { width: px2vp(postNodeWidth_px) };
      this.initTranslateX = px2vp(cardItemInfo_px.left);
    }
  }

  public doEnterAnimation(transitionProxy?: NavigationTransitionProxy): void {
    this.scaleValue = this.initScale;
    this.translateX = this.initTranslateX;
    this.clipWidth = this.initClipWidth;
    this.clipHeight = this.initClipHeight;
    this.translateY = this.initTranslateY;
    this.positionYValue = this.initPositionValueY;
    this.positionXValue = this.initPositionValueX;
    this.radius = this.initBorderRadius;
```

---

## [2/100] ID: OH_0058 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- Target File: `entry/src/main/ets/pages/group/BatchDeleteGroup.ets`
- Warning: Do not use stringify in the key generator function of LazyForEach

### Buggy Snippet
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

---

## [3/100] ID: OH_0013 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-reusable-component`
- Target File: `entry/src/main/ets/MainAbility/pages/phone/dialer/callRecord/MissedRecord.ets`
- Warning: Use reusable components to define complex components whenever possible

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

---

## [4/100] ID: OH_0380 | ArkTS (T)
- Rule ID: `@performance/foreach-args-check`
- Target File: `entry/src/main/ets/pages/example/TextLayer.ets`
- Warning: For performance purposes, set keyGenerator for ForEach.

### Buggy Snippet
```typescript
@Component
struct TextLayer {
  @State isLoading: boolean = true
  private animationPaths: string[] = [
    'common/text/000_TextAnimation_Rotation.json',
    'common/text/0707_TextAnimation_Opacity_Rotation.json',
    'common/text/7307-text-animation-yes.json',
    'common/text/10896-text-animation-sale-off.json',
    'common/text/19659-sliced-text-choose-your-fighter.json',
    'common/text/Text_Test_HELL_3_RangeSelector.json',
    'common/text/TextStrokeTest_font_136_Stroke_10_to_27.json',
    'common/text_str/text_world.json',
    'common/text_str/text.json',
    'common/text_str/text_1.json',
    'common/text_str/text_arrange.json',
    'common/text_str/text_arrange_1.json',
    'common/text_str/text_path.json',
    'common/text_str/text_path2.json',
    'common/text_str/text_path3.json',
    'common/text_str/text_shapes.json'
  ]
  private controllers: LottieController[] = []
  private context = getContext(this) as common.UIAbilityContext

  aboutToAppear() {
    try {
      // 为每个动画创建控制器
      this.controllers = Array(this.animationPaths.length)
        .fill(null)
        .map(() => new LottieController())

      this.isLoading = false
    } catch (error) {
      console.error('Failed to initialize controllers:', error)
    }
  }

  aboutToDisappear() {
    this.controllers.forEach(controller => {
      controller?.stop()
      controller?.destroy()
    })
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
      Text('Text Layer Test')
        .fontSize(24)
        .margin({ top: 20, bottom: 20 })

      if (this.isLoading) {
        this.LoadingView()
      } else {
        Scroll() {
          Grid() {
            ForEach(this.animationPaths, (path: string, index) => {
              GridItem() {
                Column() {
                  LottieView({
                    loop: true,
                    autoplay: true,
                    path: $rawfile(path),
                    controller: this.controllers[index],
                    contentMode: 'Contain'
                  })
                    .width('90%')
                    .aspectRatio(1)
                    .backgroundColor(Color.Gray)
                    .margin(10)
                    .onClick(() => {
                      this.controllers[index].togglePause()
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
          .columnsTemplate('1fr 1fr') // 使用两列布局
          .width('100%')
          .layoutWeight(1)
        }
        .scrollBar(BarState.Auto)
        .edgeEffect(EdgeEffect.Spring)
        .height('85%')
      }
    }
    .width('100%')
    .height('100%')
    .padding(20)
    .backgroundColor(Color.White)
  }
}
```

---

## [5/100] ID: OH_0141 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-transition-to-replace-animateto`
- Target File: `product/pc/notificationpanel/src/main/ets/pages/index.ets`
- Warning: Use transition for component transition animation

### Buggy Snippet
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

---

## [6/100] ID: OH_0126 | ArkTS (T)
- Rule ID: `@performance/hp-arkts-no-use-any-export-other`
- Target File: `libgif/index.ets`
- Warning: Do not use export * to export types and data defined in the other module

### Buggy Snippet
```typescript
// GIF解码数据规范
export * from './src/main/ets/components/gif/display/GIFFrame'
// GIF解码能力
export * from './src/main/ets/components/gif/parse/GIFParse'
// GIF解码部分能力增强
export * from './src/main/ets/components/gif/utils/ParseHelperUtils'
// 本地资源网络资源获取能力
export * from './src/main/ets/components/gif/utils/ResourceLoader'
// 能力增强worker 解析GIF数据
export { handler } from './src/main/ets/components/gif/worker/GifWorker'

export * from 'gifuct-js'
```

---

## [7/100] ID: OH_0115 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `entry/src/main/ets/pages/group/SelectMemberSendMessage.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

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

---

## [8/100] ID: OH_0072 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-func-as-arg-for-reusable-component`
- Target File: `entry/src/main/ets/component/contactdetail/DetailInfoRemarks.ets`
- Warning: Do not use functions as input parameters for creating reusable components

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

---

## [9/100] ID: OH_0378 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-reusable-component`
- Target File: `entry/src/main/ets/pages/example/thirdpartyscenes/Scene_4.ets`
- Warning: Use reusable components to define complex components whenever possible

### Buggy Snippet
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

---

## [10/100] ID: OH_0053 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- Target File: `entry/src/main/ets/pages/favorites/addFavoriteList.ets`
- Warning: Do not use stringify in the key generator function of LazyForEach

### Buggy Snippet
```typescript
@Component
struct ContactsList {
  @Link presenter: AddFavoriteListPresenter;
  // Scrolling Parameters
  private scroller: Scroller = GlobalContext.getContext().getObject('scroller') as Scroller;
  @State alphabetSelected: number = 0;
  @State isAlphabetClicked: boolean = false;
  @State dragList: boolean = false;
  @State alphabetIndexPresenter: AlphabetIndexerPresenter = this.presenter.alphabetIndexPresenter;
  @State isPC: boolean = EnvironmentProp.isPC();
  @StorageLink('isShowSmartWindow') isShowSmartWindow: boolean = false;
  @StorageProp('fontSizeScale') fontSizeScale: number = 0;
  @StorageProp('splitStatus') splitStatus: SplitStatus = SplitStatus.DEFAULT;
  @State preListItemNum: number = 0;
  @StorageLink('sceillOnlenth') sceillOnlenth: number = 0;
  private slidingMultipleSelectionsUtil: SlidingMultipleSelectionsUtil =
    new SlidingMultipleSelectionsUtil(this.scroller, 56);

  build() {
    Column() {
      Stack({ alignContent: Alignment.TopEnd }) {
        List({ initialIndex: this.presenter.initialIndex, scroller: this.scroller }) {
          LazyForEach(this.presenter.contactsSource, (item: BatchSelectContact) => {
            ListItem() {
              AddFavoriteItemView({
                presenter: this.presenter,
                item: item.contact,
                index: item.index,
                showIndex: item.showIndex,
                showDivifer: item.showDivifer
              })
            }
          }, (item: BatchSelectContact) => JSON.stringify(item))
        }
        .width('100%')
        .padding({ right: this.isShowSmartWindow ? $r('app.float.id_card_margin_xxl_minus') : 0 })
        .height('100%')
        .listDirection(Axis.Vertical)
        .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
        .scrollBar(BarState.Off)
        .clipContent(ContentClipMode.SAFE_AREA)
        .safeAreaPadding({ top: this.isPC ? 0 : $r('app.float.id_hds_title_margin') })
        .onScrollIndex((firstIndex: number, lastIndex: number) => {
          this.slidingMultipleSelectionsUtil.scrollStartIndex = firstIndex;
          this.slidingMultipleSelectionsUtil.scrollEndIndex = lastIndex;

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
        .gesture(PanGesture({ direction: PanDirection.Vertical })
          .onActionStart((event: GestureEvent) => {
            for (let i = 0; i < this.presenter.contactsSource.totalCount(); ++i) {
              let item = this.presenter.contactsSource.getData(i);
              let selectStatus = this.presenter.checkedStatus.has(item?.contact.contactId);
              this.slidingMultipleSelectionsUtil.oldSelectStatus[i] = selectStatus;
              this.slidingMultipleSelectionsUtil.curSelectStatus[i] = selectStatus;
            }
            this.slidingMultipleSelectionsUtil.onActionStart(event.fingerList[0]);
          })
          .onActionUpdate((event: GestureEvent) => {
            let updateIndexes = this.slidingMultipleSelectionsUtil.onActionUpdate(event.fingerList[0], (index) => {
              let curSelectStatus = false;
              if (index >= 0) {
                let item = this.presenter.contactsSource.getData(index);
                curSelectStatus = this.presenter.checkedStatus.has(item?.contact.contactId);
              }
              return curSelectStatus;
            });
            updateIndexes.forEach((index) => {
              if (index >= 0) {
                let item = this.presenter.contactsSource.getData(index);
                this.presenter.itemOnClick(item?.contact, index);
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

        if (DisplaySplitUtil.isShowIndex(this.splitStatus)) {
          AlphabetIndexerPage({
            scroller: this.scroller,
            selected: this.alphabetSelected, isClicked: $isAlphabetClicked,
            isAutoCollapse:true,
            preIndexNum: this.preListItemNum,
            scrollIndexOffset: false,
            presenter:this.presenter.alphabetIndexPresenter
          })
            .margin({ top: '118vp', bottom: '10%' })
            .visibility(this.isShowSmartWindow ? Visibility.None : Visibility.Visible)
        }
      }
    }
    .width('100%')
  }
}
```

---

## [11/100] ID: OH_0347 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-object-link-to-replace-prop`
- Target File: `entry/src/main/ets/view/ItemDescView/DescRaidersView.ets`
- Warning: Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

### Buggy Snippet
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

---

## [12/100] ID: OH_0280 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-state-var-access-in-loop`
- Target File: `feature/wifi/src/main/ets/component/WifiPrecisionComponent.ets`
- Warning: Avoid frequent state variable reads inside loop logic

### Buggy Snippet
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

---

## [13/100] ID: OH_0045 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `entry/src/main/ets/pages/favorites/favoriteList.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

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

---

## [14/100] ID: OH_0303 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-local-var-to-replace-state-var`
- Target File: `entry/src/main/ets/pages/encryptionProtection.ets`
- Warning: Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
if (this.selectedPermissionTypeEdit.data === 'all') {
      property.everyoneAccessList = [ dlpPermission.DLPFileAccess.CONTENT_EDIT ];
      this.staffDataArrayReadOnly = [];
      this.staffDataArrayEdit = [];
    } else {
      let isReadyOnlyAll = this.selectedPermissionTypeReadOnly.data === 'all';
      if (isReadyOnlyAll) {
        property.everyoneAccessList = [ dlpPermission.DLPFileAccess.READ_ONLY ];
      }
      if (this.selectedPermissionTypeReadOnly.data === 'all') {
        this.staffDataArrayReadOnly = []
      }
      if (['all', 'self'].includes(this.selectedPermissionTypeEdit.data)) {
        this.staffDataArrayEdit = [];
      }
      this.staffDataArrayReadOnly && this.staffDataArrayReadOnly.forEach(item => {
        property.authUserList?.push({
          authAccount: item.authAccount,
          dlpFileAccess: dlpPermission.DLPFileAccess.READ_ONLY,
          permExpiryTime: Date.UTC(9999, 1, 1),
          authAccountType: this.domainOrCloudAccount,
        })
      })
      this.staffDataArrayEdit && this.staffDataArrayEdit.forEach(item => {
        property.authUserList?.push({
          authAccount: item.authAccount,
          dlpFileAccess: dlpPermission.DLPFileAccess.CONTENT_EDIT,
          permExpiryTime: Date.UTC(9999, 1, 1),
          authAccountType: this.domainOrCloudAccount,
        })
      })
    }
```

---

## [15/100] ID: OH_0217 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-suggest-use-effectkit-blur`
- Target File: `product/tablet/src/main/ets/pages/PreviewArea.ets`
- Warning: Suggestion Use effectKit.createEffect to create a blur effect

### Buggy Snippet
```typescript
{
{
{
{
            Image(this.mScreenshotPixelMap)
              .width(this.xComponentWidth)
              .height(this.xComponentHeight)
              .blur(this.mModeSwitchImgBlur)
              .syncLoad(true)
          }
          .rotate(this.cameraSwitchRotation)
          .scale(this.imgScale)
          .opacity(this.mModeSwitchImgOpacity)
        }
      }

      ShowFlashBlack({ xComponentWidth: this.xComponentWidth, xComponentHeight: this.xComponentHeight })
        .hitTestBehavior(HitTestMode.Transparent)

      if (this.state.isShowNightBigText) {
        Stack({ alignContent: Alignment.Top }) {
          NightTimeBigText()
        }
        .width('100%')
        .height('100%')
        .position(this.getLayoutPosition())
        .touchable(false)
      }

      if (this.isShowBurstCaptureBigText) {
        BurstCaptureBigText()
          .width('100%')
          .height('100%')
          .position(this.getBurstLayoutPosition())
          .touchable(false)
      }

      if (this.state.isShowtimeLapse) {
        TimeLapseView()
          .position(this.isPicker ? undefined : {
            x: this.positionZero,
            y: this.getTimeLapseViewBottom()
          })
      }
    }
    .width(this.xComponentWidth)
    .height(this.xComponentHeight)
    .hitTestBehavior(HitTestMode.Transparent)
    .clip(true)
    .backgroundColor(Color.Black)
    .enabled(!this.isDownSuperSlowBtn)
    .onTouch((event: TouchEvent) => {
      if (event.type === TouchType.Move) {
        return;
      }
      if (TouchType.Down === event.type) {
        this.generateBlurPixelMap(false);
        if (event.touches.length === 2) {
          this.touchPrepareZoom();
        }
        return;
      }
      if (event.type === TouchType.Up || event.type === TouchType.Cancel) {
        if (event.touches.length === 2) {
          this.touchUnprepareZoom();
        }
      }
    })
    .gesture(
      GestureGroup(
        GestureMode.Exclusive,
        TapGesture({ fingers: 1, count: 1 })
          .onAction(() => this.onPreviewClicked()),
        PinchGesture({ fingers: 2, distance: 1 })
          .onActionStart((event?: GestureEvent) => {
            if (!event || this.isNightShutting) {
              return;
            }
            return this.pinchGestureStart(event);
          })
          .onActionUpdate((event?: GestureEvent) => {
            if (!event || this.isNightShutting) {
              return;
            }
            return this.pinchGestureUpdate(event);
          })
          .onActionCancel(() => {
            HiLog.i(TAG, 'onActionCancel');
            this.pinchGestureEnd();
          })
          .onActionEnd((event?: GestureEvent) => {
            if (!event || this.isNightShutting) {
              return;
            }
            return this.pinchGestureEnd();
          }),
        PanGesture({
          fingers: 1,
          direction: PanDirection.Up,
          distance: 10
        })
          .onActionStart((): void => {
            if (this.state.uiEnable && !this.state.isShowtimeLapse && this.state.videoState === RecordingState.READY &&
              !this.state.isShowNightBigText && !this.isDownSuperSlowBtn && !this.isShowNightInfo &&
              !this.isProShuttering) {
              this.mAction.swipeChangeMode(1);
            }
          }),
        PanGesture({
          fingers: 1,
          direction: PanDirection.Down,
          distance: 10
        })
          .onActionStart((): void => {
            if (this.state.uiEnable && !this.state.isShowtimeLapse && this.state.videoState === RecordingState.READY &&
              !this.state.isShowNightBigText && !this.isDownSuperSlowBtn && !this.isShowNightInfo &&
              !this.isProShuttering) {
              this.mAction.swipeChangeMode(-1);
            }
          })
      )
    )
  }

  private touchPrepareZoom(): void {
    this.mAction.changeFunctionValue(FunctionId.ZOOM, {
      zoomRatio: undefined,
      isPrepareZoom: true
    } as ZoomFuncValueStruct);
  }

  private touchUnprepareZoom(): void {
    this.mAction.changeFunctionValue(FunctionId.ZOOM, {
      zoomRatio: undefined,
      isUnprepareZoom: true,
      unprepareDelay: ZoomParam.UNPREPARE_DELAY_TIME
    } as ZoomFuncValueStruct);
  }

  public onScaleUpdate(scale: number): void {
    HiLog.i(TAG, `onScaleUpdate called scale = ${scale}.`);
    let tempZoom = 1.0;
    if (scale > 1) {
      tempZoom = this.state.baseZoom + scale - 1;
    } else {
      tempZoom = this.state.baseZoom * scale;
    }
    if (Math.abs(tempZoom - this.state.zoomRatio) >= 0.1) {
      if (tempZoom >= this.state.minZoomRatio && tempZoom <= this.state.maxZoomRatio) {
        this.mAction.changeFunctionValue(FunctionId.ZOOM, {
          zoomRatio: tempZoom,
        } as ZoomFuncValueStruct);
      }
    }
```

---

## [16/100] ID: OH_0017 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-reusable-component`
- Target File: `entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets`
- Warning: Use reusable components to define complex components whenever possible

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

---

## [17/100] ID: OH_0016 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `entry/src/main/ets/pages/contacts/batchselectcontacts/BatchSelectContactsPage.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

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

---

## [18/100] ID: OH_0048 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `entry/src/main/ets/pages/contacts/batchselectcontacts/SingleSelectContactPage.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

### Buggy Snippet
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

---

## [19/100] ID: OH_0112 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- Target File: `entry/src/main/ets/pages/contacts/settings/RecentDelete.ets`
- Warning: Do not use stringify in the key generator function of LazyForEach

### Buggy Snippet
```typescript
@Component
struct RecentDeleteContactList {
  @Link presenter: RecentDeletePresenter;
  @StorageLink('breakpoint') curBp: string = 'sm';
  @StorageProp('fontSizeScale') fontSizeScale: number = 0;
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;
  @StorageProp(AccessibilityUtil.ISOPENACCESSIBILITY) isOpenAccessibility: boolean = false;
  private scroller: Scroller = GlobalContext.getContext().getObject('scrollerRecentDeleteContacts') as Scroller;
  private slidingMultipleSelectionsUtil: SlidingMultipleSelectionsUtil =
    new SlidingMultipleSelectionsUtil(this.scroller, 56);


  aboutToAppear(): void {
    this.slidingMultipleSelectionsUtil.isSliding = this.presenter.selectRecentDeleteChange;
  }


  build() {
    Column() {
      List({ space: 0, initialIndex: 0, scroller: this.scroller }) {
          LazyForEach(this.presenter.recentDeleteDataSource, (item: RecentDeleteBean, index: number) => {
            ListItem() {
              RecentDeleteItem({
                item: item,
                index: index,
                presenter: this.presenter,
                isThemeActive: this.isThemeActive,
              })
            }
            .accessibilityLevel(this.presenter.selectRecentDeleteChange ? 'no' : 'yes')
            .onClick(() => {
              if (!this.presenter.selectRecentDeleteChange) {
                return;
              }
              HiLog.w(TAG, 'onClick listitem: ' + item.id.toString());
              this.presenter.itemOnClick(item, index);
            })
            .gesture(
              LongPressGesture({ repeat: false })
                .onAction((event?: GestureEvent) => {
                  this.presenter.processLongPressedItem(item, index);
                })
            )
            .onMouse((event: MouseEvent) => {
              if (event.button == MouseButton.Right && event.action == MouseAction.Release) {
                this.presenter.processLongPressedItem(item, index);
              }
            })
          }, (item: RecentDeleteBean, index: number) => JSON.stringify(item) + index.toString())
      }
      .listDirection(Axis.Vertical)
      .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
      .scrollBar(BarState.Off)
      .cachedCount(3)
      .backgroundColor($r('app.color.skin_ohos_id_color_list_card_bg'))
      .borderRadius($r('sys.float.corner_radius_level10'))
      .margin({
        left: this.curBp === 'lg' ? $r('app.float.id_card_margin_max') : $r('app.float.id_card_margin_xxl'),
        right: this.curBp === 'lg' ? $r('app.float.id_card_margin_max') : $r('app.float.id_card_margin_xxl')
      })
      .divider({
        strokeWidth: '1px',
        color: $r('app.color.skin_ohos_id_color_list_separator'),
        startMargin: $r('app.float.id_card_margin_large'),
        endMargin: $r('app.float.id_card_margin_large')
      })
      .onTouch(() => {
        this.slidingMultipleSelectionsUtil.isSliding = this.presenter.selectRecentDeleteChange;
      })
      .onScrollIndex((firstIndex: number, lastIndex: number) => {
        this.slidingMultipleSelectionsUtil.scrollStartIndex = firstIndex;
        this.slidingMultipleSelectionsUtil.scrollEndIndex = lastIndex;
      })
      .gesture(PanGesture({ direction: PanDirection.Vertical })
        .onActionStart((event: GestureEvent) => {
          for (let i = 0; i < this.presenter.recentDeleteDataSource.totalCount(); ++i) {
            let item = this.presenter.recentDeleteDataSource.getData(i);
            let selectStatus = this.presenter.checkedStatus.has(item?.id);
            this.slidingMultipleSelectionsUtil.oldSelectStatus[i] = selectStatus;
            this.slidingMultipleSelectionsUtil.curSelectStatus[i] = selectStatus;
          }
          this.slidingMultipleSelectionsUtil.onActionStart(event.fingerList[0]);
        })
        .onActionUpdate((event: GestureEvent) => {
          let updateIndexes = this.slidingMultipleSelectionsUtil.onActionUpdate(event.fingerList[0], (index) => {
            let curSelectStatus = false;
            if (index >= 0) {
              let item = this.presenter.recentDeleteDataSource.getData(index);
              curSelectStatus = this.presenter.checkedStatus.has(item?.id);
            }
            return curSelectStatus;
          });
          updateIndexes.forEach((index) => {
            if (index >= 0) {
              let item = this.presenter.recentDeleteDataSource.getData(index);
              this.presenter.itemOnClick(item, index);
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
    .layoutWeight(1)
    .flexShrink(1)
  }
}
```

---

## [20/100] ID: OH_0120 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-state-var-access-in-loop`
- Target File: `entry/src/main/ets/card/pages/ShortcutEditPage.ets`
- Warning: Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (const item of this.deleteContact) {
        if (item.contactId && this.contactId !== item.contactId) {
          item.formId = await this.common.queryContactFormId(item.contactId, this.context)
          item.formId = item.formId.split('//').filter(item => !item.includes(this.formId)).join('//')
          this.common.updateContactFormId(item.contactId, this.context, item.formId)
        }
      }
```

---

## [21/100] ID: OH_0259 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-object-link-to-replace-prop`
- Target File: `product/phone/src/main/ets/pages/biometricsandpassword/component/MenuComponent.ets`
- Warning: Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

### Buggy Snippet
```typescript
@Component
struct EntryComponent {
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
    .borderRadius($r('sys.float.corner_radius_level8'))
  }

  build() {
    Column() {
      Flex({ direction: FlexDirection.Row, justifyContent: FlexAlign.SpaceBetween, alignItems: ItemAlign.Center }) {
        Column() {
          Text(this.menu?.title)
            .fontColor(this.menu?.style?.fontColor ? this.menu.style.fontColor : $r('sys.color.ohos_id_color_text_primary'))
            .fontSize(this.menu?.style?.fontSize ? this.menu.style.fontSize : $r('sys.float.ohos_id_text_size_body1'))
            .fontWeight(this.menu?.style?.fontWeight ? this.menu.style.fontWeight : FontWeight.Medium)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
            .maxLines(MAX_LINES_10);
        }
        .padding({
          top: FontScaleUtils.getCurrentTopPadding(),
          bottom: FontScaleUtils.getCurrentTopPadding()
        })
        .flexGrow(1)
        .alignItems(HorizontalAlign.Start);

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
      .flexStyle()
      .hoverEffect(HoverEffect.Highlight)
      .stateStyles({
        normal: this.normalStyles,
        pressed: this.pressedStyles,
      })
      .focusBox({
        margin: FOCUS_BOX_PADDING_METRICS
      })
      .onClick(() => {
        if (this.menu?.onMenuClick) {
          this.menu?.onMenuClick(this.index);
        }
      })
    }.padding({
      left: $r('app.float.padding_4'),
      right: $r('app.float.padding_4'),
      top: $r('app.float.margin_0'),
      bottom: $r('app.float.margin_0')
    })
  }
}
```

---

## [22/100] ID: OH_0309 | ArkTS (T)
- Rule ID: `@previewer/mandatory-default-value-for-local-initialization`
- Target File: `HMRouterExamples/commons/ui_components/src/main/ets/components/CellComponent.ets`
- Warning: If a component attribute supports local initialization, a valid, runtime-independent default value should be set for it.

### Buggy Snippet
```typescript
@Component
export struct Cell {
  @Require private title: string | Resource | undefined;
  private description: string | Resource | undefined;
  private isLink: boolean = false;
  click: () => void = () => {
  };

  build() {
    Row() {
      Column() {
        Text(this.title)
          .fontSize($r("app.float.font_md"))
          .fontColor($r("app.color.text_primary"))
          .maxLines(1)
          .fontWeight(FontWeight.Bold)
          .constraintSize({
            maxWidth: "70%"
          })
          .textOverflow({ overflow: TextOverflow.Ellipsis });

        if (this.description) {
          Text(this.description)
            .fontSize($r("app.float.font_sm"))
            .fontColor($r("app.color.text_secondary"))
            .maxLines(1)
            .constraintSize({
              maxWidth: "70%"
            })
            .textOverflow({ overflow: TextOverflow.Ellipsis });
        }
      }.height($r("app.float.cell_min_height")).justifyContent(FlexAlign.SpaceAround).alignItems(HorizontalAlign.Start);

      Blank().layoutWeight(1);
      if (this.isLink) {
        Text($r("app.string.more")).fontSize($r("app.float.font_sm")).fontColor($r("app.color.text_secondary"));
        Image($r("app.media.chevron_right")).width(12).height(24);
      }
    }
    .width("100%")
    .backgroundColor($r("app.color.color_white"))
    .padding($r("app.float.vp_12"))
    .margin({ left: $r("app.float.vp_12"), right: $r("app.float.vp_12") })
    .onClick(() => {
      this.click();
    });
  }
}
```

---

## [23/100] ID: OH_0014 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `entry/src/main/ets/pages/dialer/callRecord/AllRecord.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

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

---

## [24/100] ID: OH_0288 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `entry/src/main/ets/pages/LazyForEachApng.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

### Buggy Snippet
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

---

## [25/100] ID: OH_0102 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- Target File: `entry/src/main/ets/pages/intelligencegroup/IntelligenceGroupSelectMemSendMsg.ets`
- Warning: Do not use stringify in the key generator function of LazyForEach

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

---

## [26/100] ID: OH_0367 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-state-var-access-in-loop`
- Target File: `vlayout/src/main/ets/components/common/StaggeredGridLayoutHelper.ets`
- Warning: Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let i = 0;i < this.vLayoutData.length; i++) {
        if (this.staggeredGridInfo.lanes && i < this.staggeredGridInfo.lanes && this.itemWidth) { //确定第一行
          if (this.staggeredGridInfo.gap != 0 && this.staggeredGridInfo.vGap == 0 && this.staggeredGridInfo.hGap == 0 &&this.staggeredGridInfo.gap) { //gap行列间距定义了
            (this.vLayoutData[i] as layoutDataType).top = this.staggeredGridInfo.gap;
            (this.vLayoutData[i] as layoutDataType).left = (this.itemWidth + this.staggeredGridInfo.gap) * i + this.staggeredGridInfo.gap;
            colHeightArray.push(this.itemHeightArray[i] + this.staggeredGridInfo.gap);
          } else if (this.staggeredGridInfo.gap == 0 && this.staggeredGridInfo.vGap != 0 && this.staggeredGridInfo.hGap == 0 && this.staggeredGridInfo.vGap) { //vGap行间距定义了
            (this.vLayoutData[i] as layoutDataType).top = this.staggeredGridInfo.vGap;
            (this.vLayoutData[i] as layoutDataType).left = (this.itemWidth) * i;
            colHeightArray.push(this.itemHeightArray[i] + this.staggeredGridInfo.vGap);
          } else if (this.staggeredGridInfo.gap == 0 && this.staggeredGridInfo.vGap == 0 && this.staggeredGridInfo.hGap != 0 && this.staggeredGridInfo.hGap) { //hGap列间距定义了
            (this.vLayoutData[i] as layoutDataType).top = 0;
            (this.vLayoutData[i] as layoutDataType).left = (this.itemWidth + this.staggeredGridInfo.hGap) * i + this.staggeredGridInfo.hGap;
            colHeightArray.push(this.itemHeightArray[i]);
          } else if (this.staggeredGridInfo.gap == 0 && this.staggeredGridInfo.vGap != 0 && this.staggeredGridInfo.hGap != 0 && this.staggeredGridInfo.hGap && this.staggeredGridInfo.vGap) { //vGap行间距、hGap列间距同时定义了
            (this.vLayoutData[i] as layoutDataType).top = this.staggeredGridInfo.vGap;
            (this.vLayoutData[i] as layoutDataType).left = (this.itemWidth + this.staggeredGridInfo.hGap) * i + this.staggeredGridInfo.hGap;
            colHeightArray.push(this.itemHeightArray[i] + this.staggeredGridInfo.vGap);
          } else if (this.staggeredGridInfo.gap == 0 && this.staggeredGridInfo.vGap == 0 && this.staggeredGridInfo.hGap == 0) { //gap、vGap、hGap同时未定义
            (this.vLayoutData[i] as layoutDataType).top = 0;
            (this.vLayoutData[i] as layoutDataType).left = (this.itemWidth) * i;
            colHeightArray.push(this.itemHeightArray[i]);
          } else if (this.staggeredGridInfo.gap) { //三个都定义，只走gap
            (this.vLayoutData[i] as layoutDataType).top = this.staggeredGridInfo.gap;
            (this.vLayoutData[i] as layoutDataType).left = (this.itemWidth + this.staggeredGridInfo.gap) * i + this.staggeredGridInfo.gap;
            colHeightArray.push(this.itemHeightArray[i] + this.staggeredGridInfo.gap);
          }
        } else if (this.staggeredGridInfo.lanes) {
          //其它行 先找到数组中的最小高度以及它的索引
          let minHeight = colHeightArray[0] //定义最小的高度
          let index = 0 //定义最小高度的下标
}
}
```

---

## [27/100] ID: OH_0333 | ArkTS (T)
- Rule ID: `@hw-stylistic/quotes`
- Target File: `HMRouterExamples/product/phone/src/main/ets/constants/RouterPageConstant.ets`
- Warning: Strings must use single quotes.

### Buggy Snippet
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
  static readonly MAIN_CASE: MainPageListItem[] = [
    {
      title: '路由跳转及拦截跳转场景',
      description: '展示路由路由跳转与使用拦截器拦截路由跳转',
      pathInfo: { pageUrl: 'RouterMainPage' }
    },
    {
      title: '生命周期配置使用场景',
      description: '展示页面生命周期的使用与常见使用场景',
      pathInfo: { pageUrl: 'LifecycleMainPage' }
    },
    {
      title: '转场动画配置使用场景',
      description: '展示页面转场动画的配置与使用',
      pathInfo: { pageUrl: 'AnimationMainPage' }
    },
    {
      title: '一次开发多端部署',
      description: '展示HMNavigation一多场景下的使用场景',
      pathInfo: { pageUrl: 'LayoutMainPage' }
    },
    {
      title: '其他使用场景',
      description: '其他使用案例，如自定义模板使用',
      pathInfo: { pageUrl: 'OtherMainPage' }
    }
  ];
}
```

---

## [28/100] ID: OH_0360 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-state-var-access-in-loop`
- Target File: `feature/pagedesktop/src/main/ets/default/common/components/SwiperPage.ets`
- Warning: Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let i = 0;i < column; i++) {
      this.ColumnsTemplate += '1fr '
    }
```

---

## [29/100] ID: OH_0215 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-state-var-access-in-loop`
- Target File: `features/extend/src/main/ets/commonfunc/exposure/LandscapeExposureBarView.ets`
- Warning: Avoid frequent state variable reads inside loop logic

### Buggy Snippet
```typescript
for (let i = 0; i < this.spotCount; i++) {
        const commonPosition: number = this.bothSidesPadding + this.longWhiteLineHeight / 2 + Math.floor(i /
        this.gapNumInEachSeg) * this.segLength + (i % this.gapNumInEachSeg) * this.dotDistance;
        const curRedLineInNum = this.valuesRange.findIndex(index => {
          return Number(index) === this.sliderValue;
        }) * this.gapNumInEachSeg;
        const initIndex = this.valuesRange.length - 1 - this.valuesRange.findIndex((item, index) => {
          return index === this.sliderValue;
        })
        if (i === 0 || i === this.spotCount - 1 || (!this.isSliding && i === curRedLineInNum) || i %
        this.gapNumInEachSeg === 0 || i === initIndex) {
          this.redrawCanvasText(i, initIndex, commonPosition);
        }
        if (i % this.gapNumInEachSeg === 0) {
          this.sliderOffCanvasCtx.globalAlpha = 1;
          this.sliderOffCanvasCtx.fillStyle = '#ffffff';
          this.sliderOffCanvasCtx.shadowColor = '#4d000000';
          this.sliderOffCanvasCtx.shadowBlur = 3;
          this.sliderOffCanvasCtx.fillRect(this.sliderCanvasWidth - this.mRightPadding - this.longWhiteLineWidth,
            commonPosition - this.longWhiteLineHeight / 2, this.longWhiteLineWidth, this.longWhiteLineHeight);
        } else {
          this.sliderOffCanvasCtx.globalAlpha = 0.6;
          this.sliderOffCanvasCtx.shadowColor = '#33000000';
          this.sliderOffCanvasCtx.shadowBlur = 3;
          this.sliderOffCanvasCtx.fillRect(this.sliderCanvasWidth - this.mRightPadding - this.shortWhiteLineWidth,
            commonPosition - this.shortWhiteLineHeight / 2, this.shortWhiteLineWidth, this.shortWhiteLineHeight);
        }
      }
```

---

## [30/100] ID: OH_0113 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `entry/src/main/ets/pages/ringtoneSelection/RingtoneIndex.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

### Buggy Snippet
```typescript
Scroll(this.mainScroller) {
            List() {
              ListItemGroup() {
                ListItem() {
                  // 选择本地音乐
                  this.SelectRingtoneBuilder();
                }

                ListItem() {
                  // 系统来电铃声
                  this.SysRingtoneBuilder();
                }

                ListItem() {
                  // 系统铃声
                  this.SysRingtoneTextBuilder();
                }

                LazyForEach(this.ringtoneFullDataList, (item: ToneAttrs, index: number) => {
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
                  .borderRadius({
                    topLeft: index === 0 ? $r('sys.float.corner_radius_level10') : undefined,
                    topRight: index === 0 ? $r('sys.float.corner_radius_level10') : undefined,
                    bottomLeft: (index === this.ringtoneFullDataList?.ringtoneArray.length - 1) ?
                    $r('sys.float.corner_radius_level10') : undefined,
                    bottomRight: (index === this.ringtoneFullDataList?.ringtoneArray.length - 1) ?
                    $r('sys.float.corner_radius_level10') : undefined
                  })
                  .backgroundColor($r('app.color.skin_ohos_id_color_card_bg'))
                }, (item: ToneAttrs) => item?.title)

                ListItem() {
                  this.NoRingToneBuilder()
                }
              }
              .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])

              ListItem() {
              }
              .padding({
                bottom: '16vp'
              })
            }
          }
```

---

## [31/100] ID: OH_0230 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-reusable-component`
- Target File: `entry/src/main/ets/pages/favoritepage/favorite.ets`
- Warning: Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
ListItem() {
                RelativeContainer() {
                  if (this.isShowHead) {
                    if (item.senderNumber) {
                      if (item?.isChatbotMessage) {
                        ContactAvatar({
                          rawContactId: '',
                          contactId: '',
                          item: item
                        })
                          .margin(this.textDirection === 'rtl' ?
                            {
                              top: 16,
                              right: this.isPC ? 24 : this.isPad ? this.padMargin : $r('sys.float.margin_right')
                            } :
                            {
                              top: 16,
                              left: this.isPC ? 24 : this.isPad ? this.padMargin : $r('sys.float.margin_left')
                            })
                          .id('favorite_list_avatar')
                          .onClick(() => {
                            this.pageInfos.pushPathByName('RcsDetailsChatbotActivity', {
                              id: item.senderNumber,
                              icon: ''
                            } as LooseObject);
                            DotUtil.getInstance().reportEvent(dotNoNeedParmas,
                              dotCommon.eventName.OPEN_CHATBOT_DETAIL);
                          })
                      } else {
                      ContactAvatar({
                        hasYellowPageIcon: this.mFavoriteCtrl
                          .nameAndPicture(item.senderNumber)?.hasYellowPageIcon,
                        yellowPageId: this.mFavoriteCtrl
                          .nameAndPicture(item.senderNumber)?.yellowPageId,
                        rawContactId: this.mFavoriteCtrl.contactIdMap.get(item.senderNumber) ?? '',
                        contactId: this.mFavoriteCtrl.contactIdMap.get(item.senderNumber) ?? '',
                        item: item,
                      })
                        .onClick(() => {
                          this.mFavoriteCtrl.titleBarAvatar(this.context, item.senderNumber);
                        })
                        .margin(this.textDirection === 'rtl' ?
                          {
                            top: 16,
                            right: this.isPC ? 24 : this.isPad ? this.padMargin : $r('sys.float.margin_right')
                          } :
                          {
                            top: 16,
                            left: this.isPC ? 24 : this.isPad ? this.padMargin : $r('sys.float.margin_left')
                          })
                        .id('favorite_list_avatar')
                      }
                    } else {
                      ContactAvatar({
                        rawContactId: this.mFavoriteCtrl.nameNoPicture('')?.rawContactId,
                        contactId: this.mFavoriteCtrl.nameNoPicture('')?.contactId,
                        item: item
                      })
                        .margin(this.textDirection === 'rtl' ?
                          {
                            top: 16,
                            right: this.isPC ? 24 : this.isPad ? this.padMargin : $r('sys.float.margin_right')
                          } :
                          {
                            top: 16,
                            left: this.isPC ? 24 : this.isPad ? this.padMargin : $r('sys.float.margin_left')
                          })
                        .id('favorite_list_avatar')
                    }
                  }
                  FavoriteName({
                    hasYellowPageIcon: this.mFavoriteCtrl
                      .nameAndPicture(item.senderNumber)?.hasYellowPageIcon,
                    item: item,
                    isPad: this.isPad,
                    isShowHead: this.isShowHead,
                    textDirection: this.textDirection,
                  })
                  if (item.msgType === 0 || item.msgType === 2) {
                    bubbleText({
                      conversationCtrl: $mFavoriteCtrl,
                      content: item.msgContent,
                      item: item,
                      itemIndex: index,
                      bubbleTextBackgroundColor: item.isSender === 0
                        ? $r('app.color.brand') : $r('sys.color.ohos_id_color_card_bg'),
                      isAdvancedSecurity: item.isAdvancedSecurity,
                      isSender: item.isSender,
                      detectResContent: item.detectResContent,
                      textDirection: this.textDirection,
                      listScroller :this.listScroller,
                      scrollEndIndex: this.scrollEndIndex,
                      scrollStartIndex: this.scrollStartIndex,
                      menuMultSelect: ((selectIndex) => {
                        this.multiSelectFlag = Visibility.Visible;
                        this.mFavoriteCtrl.listCheckBoxChange(index, true);
                      }),
                      menuDeleteCallBack: ((deleteItem) => {
                        this.longPressDeleteItem = deleteItem;
                        this.mFavoriteCtrl.clickLongPressDelete();
                        this.delConversionController.open();
                      })
                    }).margin({ top: 4, bottom: 8 })
                      .alignRules(this.favoriteContentAlignRules)
                      .id('favorite_list_content')
                  }
                  else if (item.msgType === 1) {
                    if (MmsUtil.isSlideType(item.contentType)) {
                      FavoriteSlideComponent({
                        itemIndex: index,
                        item: item,
                        listScroller :this.listScroller,
                        scrollEndIndex: this.scrollEndIndex,
                        scrollStartIndex: this.scrollStartIndex,
                        menuMultSelect: ((selectIndex) => {
                          this.multiSelectFlag = Visibility.Visible;
                          this.mFavoriteCtrl.listCheckBoxChange(selectIndex, true);
                        }),
                        menuDeleteCallBack: ((deleteItem) => {
                          this.longPressDeleteItem = deleteItem;
                          this.mFavoriteCtrl.clickLongPressDelete();
                          this.delConversionController.open();
                        })
                      }).alignRules(this.favoriteContentAlignRules)
                        .id('favorite_list_content')
                    } else if (this.mFavoriteCtrl.mmsScreening(item.msgId, 8)) { //彩信位置消息
                      this.buildMmsContentMap(item, index, 'favorite_list_content')
                    } else if (!item.msgContent &&
                    this.mFavoriteCtrl.mmsScreening(item.msgId, 1)) {
                      MmsContentImage({
                        imageProps: this.mFavoriteCtrl.mmsScreening(item.msgId, 1).locationPath ?? '',
                        ct: this.mFavoriteCtrl.mmsScreening(item.msgId, 1).ct ?? '',
                        screenWidth: this.screenWidth,
                        itemIndex: index,
                        item: item,
                        listScroller :this.listScroller,
                        scrollEndIndex: this.scrollEndIndex,
                        scrollStartIndex: this.scrollStartIndex,
                        menuMultSelect: ((selectIndex) => {
                          this.multiSelectFlag = Visibility.Visible;
                          this.mFavoriteCtrl.listCheckBoxChange(selectIndex, true);
                        }),
                        menuDeleteCallBack: ((deleteItem) => {
                          this.longPressDeleteItem = deleteItem;
                          this.mFavoriteCtrl.clickLongPressDelete();
                          this.delConversionController.open();
                        })
                      }).alignRules(this.favoriteContentAlignRules)
                        .id('favorite_list_content')
                    }
}
}
}
```

---

## [32/100] ID: OH_0302 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-local-var-to-replace-state-var`
- Target File: `entry/src/main/ets/pages/encryptionProtection.ets`
- Warning: Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
tempData() {
    let accountInfo: osAccount.OsAccountInfo = GlobalContext.load('accountInfo');
    let property: dlpPermission.DLPProperty = GlobalContext.load('dlpProperty') !== undefined ? GlobalContext.load('dlpProperty') : defaultDlpProperty;
    this.staffDataArrayReadOnly = removeDuplicate(this.staffDataArrayReadOnly, 'authAccount');
    this.staffDataArrayEdit = removeDuplicate(this.staffDataArrayEdit, 'authAccount');
    this.staffDataArrayReadOnly = this.staffDataArrayReadOnly.filter((item) =>!this.staffDataArrayEdit.some((ele) => ele.authAccount === item.authAccount));
    if (GlobalContext.load('domainAccount') as boolean) {
      property.ownerAccount = accountInfo.domainInfo.accountName;
      property.ownerAccountID = accountInfo.domainInfo.accountId ?? '';
    } else {
      property.ownerAccount = accountInfo.distributedInfo.name;
      property.ownerAccountID = accountInfo.distributedInfo.id;
    }
    property.authUserList = [];
    property.everyoneAccessList = [];
    property.offlineAccess = this.selectedIndex === 0 ? true : false;
    property.expireTime = this.selectedIndex === 0 ? 0 : this.reconfigurationTime(this.validity).getTime();
    if (this.selectedPermissionTypeEdit.data === 'all') {
      property.everyoneAccessList = [ dlpPermission.DLPFileAccess.CONTENT_EDIT ];
      this.staffDataArrayReadOnly = [];
      this.staffDataArrayEdit = [];
    } else {
      let isReadyOnlyAll = this.selectedPermissionTypeReadOnly.data === 'all';
      if (isReadyOnlyAll) {
        property.everyoneAccessList = [ dlpPermission.DLPFileAccess.READ_ONLY ];
      }
      if (this.selectedPermissionTypeReadOnly.data === 'all') {
        this.staffDataArrayReadOnly = []
      }
      if (['all', 'self'].includes(this.selectedPermissionTypeEdit.data)) {
        this.staffDataArrayEdit = [];
      }
      this.staffDataArrayReadOnly && this.staffDataArrayReadOnly.forEach(item => {
        property.authUserList?.push({
          authAccount: item.authAccount,
          dlpFileAccess: dlpPermission.DLPFileAccess.READ_ONLY,
          permExpiryTime: Date.UTC(9999, 1, 1),
          authAccountType: this.domainOrCloudAccount,
        })
      })
      this.staffDataArrayEdit && this.staffDataArrayEdit.forEach(item => {
        property.authUserList?.push({
          authAccount: item.authAccount,
          dlpFileAccess: dlpPermission.DLPFileAccess.CONTENT_EDIT,
          permExpiryTime: Date.UTC(9999, 1, 1),
          authAccountType: this.domainOrCloudAccount,
        })
      })
    }

    let authUserListNew: IAuthUser[] = [];
    property.authUserList.forEach(item => {
      authUserListNew.push(
        new IAuthUser(
          item.authAccount,
          item.authAccountType,
          item.dlpFileAccess,
          item.permExpiryTime
        )
      )
    })
    let _dlp = new IDLDLPProperty(
      property.ownerAccount,
      property.ownerAccountID,
      property.ownerAccountType,
      authUserListNew,
      property.contactAccount,
      property.offlineAccess,
      property.everyoneAccessList,
      property.expireTime
    );
    return _dlp;
  }
```

---

## [33/100] ID: OH_0143 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-transition-to-replace-animateto`
- Target File: `product/pc/notificationpanel/src/main/ets/pages/index.ets`
- Warning: Use transition for component transition animation

### Buggy Snippet
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
    EventManager.subscribe(SHOW_EVENT, () => this.showWindow()),
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
      let dis = await display.getDefaultDisplaySync();
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
          : this.showWindow();
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

  showWindow() {
    Log.showInfo(TAG, `do show window.`);
    WindowManager.showWindow(WindowType.NOTIFICATION_PANEL)
    this.showAnimation()
  }
}
```

---

## [34/100] ID: OH_0004 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `entry/src/main/ets/MainAbility/pages/dialer/callRecord/AllRecord.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

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

---

## [35/100] ID: OH_0082 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-reusable-component`
- Target File: `entry/src/main/ets/pages/group/GroupList.ets`
- Warning: Use reusable components to define complex components whenever possible

### Buggy Snippet
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

---

## [36/100] ID: OH_0358 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-reusable-component`
- Target File: `entry/src/main/ets/pages/ShortVideoPage.ets`
- Warning: Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
struct ShortVideoPage {
  @State @Watch('curIndexChangeOn') curIndex: number = 0;
  @State firstFlag: boolean = true;
  @State isPageShow: boolean = false;
  @State foldStatus: number = 0;
  @Provide isFirstAVPlayer: boolean = true;
  @StorageProp(CommonConstants.UI_CONTEXT_STORAGE_KEY) uiContext: UIContext =
    AppStorage.get(CommonConstants.UI_CONTEXT_STORAGE_KEY) as UIContext;
  private swiperController: SwiperController = new SwiperController();
  private typeCfg: TypeReuseConfig = {
    type: SceneType.XCOMPONENT,
    expirationTime: 30 * 60 * 1000, // 节点过期时间（毫秒）
    reuseCallback: this.reuseCallback,
    recycleCallback: this.recycleCallback
  }
  private sourceData = new AVDataSource(Const.VIDEO_SOURCE);

  curIndexChangeOn() {
    for (let i = 0; i < this.sourceData.totalCount(); i++) {
      let tmpData = videoData[i]
      if (tmpData.curIndex === this.curIndex) {
        Logger.debug(TAG,
          `curIndexChangeOn state:${tmpData.avPlayer.state}, url:${tmpData.avPlayer.url}, curIndex:${this.curIndex}`)
        if (tmpData.avPlayer.state === AVPlayerState.PREPARED || tmpData.avPlayer.state === AVPlayerState.PAUSED ||
          tmpData.avPlayer.state === AVPlayerState.COMPLETED) {
          tmpData.avPlayer.play()
        } else if (tmpData.avPlayer.state === AVPlayerState.PLAYING) {
          tmpData.avPlayer.pause()
          tmpData.avPlayer.play()
        } else {
          // 播放重试，如果是init状态则需要等到prepared状态才能执行play播放
          Logger.error(TAG,
            `curIndexChangeOn state error:${tmpData.avPlayer.state}, url:${tmpData.avPlayer.url}, curIndex:${this.curIndex}`)
          let intervalFlag = setInterval(async () => {
            if (tmpData.avPlayer.state === AVPlayerState.PREPARED) {
              tmpData.avPlayer.play()
              clearInterval(intervalFlag);
            }
          }, 10);
        }
      } else {
        Logger.debug(TAG,
          `curIndexChangeOn else state:${tmpData.avPlayer.state}, url:${tmpData.avPlayer.url}, curIndex:${this.curIndex}`)
        if (tmpData.avPlayer.state === AVPlayerState.PLAYING) {
          Logger.debug(TAG, `avplayer set to pause, current state:${tmpData.avPlayer.state}, i:${i}`)
          tmpData.avPlayer.pause()
        }
      }
    }
  }

  async aboutToAppear(): Promise<void> {
    nodePoolVideo.setTypeReuseConfig(this.typeCfg);
    display.on('foldStatusChange', (foldStatus: display.FoldStatus) => {
      this.foldStatus = foldStatus;
      Logger.debug(TAG, `FoldStatusChange:${this.foldStatus}.`);
    })
  }

  async onPageHide(): Promise<void> {
    Logger.debug(TAG, `onPageHide curIndex: ${this.curIndex}`);
    for (let i = 0; i < this.sourceData.totalCount(); i++) {
      let tmpData = videoData[i]
      Logger.debug(TAG,
        `onPageHide state:${tmpData.avPlayer.state}, url:${tmpData.avPlayer.url}, curIndex:${this.curIndex}`)
      if (tmpData.avPlayer.state === AVPlayerState.PLAYING) {
        Logger.debug(TAG, `onPageHide avplayer set to pause, current state:${tmpData.avPlayer.state}, i:${i}`)
        tmpData.avPlayer.pause()
      }
    }

    let context = this.uiContext.getHostContext();
    if (context) {
      let windowClass = await window.getLastWindow(context);
      windowClass.setWindowSystemBarProperties({
        statusBarContentColor: '#000000'
      });
    } else {
      Logger.error(TAG, 'Host context is undefined.');
    }
  }

  async onPageShow(): Promise<void> {
    Logger.debug(TAG, `onPageShow curIndex: ${this.curIndex}`);
    this.curIndexChangeOn();

    let context = this.uiContext.getHostContext();
    if (context) {
      let windowClass = await window.getLastWindow(context);
      windowClass.setWindowSystemBarProperties({
        statusBarContentColor: '#FFFFFF'
      });
    } else {
      Logger.error(TAG, 'Host context is undefined.');
    }
  }

  build() {
    Swiper(this.swiperController) {
      LazyForEach(this.sourceData, (videoSource: string, index: number) => {
        NodeContainerProxy({
          nodeItem: nodePoolVideo.getNode(
            SceneType.XCOMPONENT,
            {
              url: videoSource,
              controller: videoData[index].controller,
              avPlayer: videoData[index].avPlayer,
              curIndex: this.curIndex,
              index: index,
            },
            videoItemWrapper,
            (data: AVPlayerXComponentData) => {
              return data.url === videoSource;
            }
          )
        })
      }, (item: string, index: number) => JSON.stringify(item) + index)
    }
    .cachedCount(3)
    .width('100%')
    .height('100%')
    .vertical(true)
    .loop(true)
    .curve(Curve.Ease)
    .duration(300)
    .indicator(false)
    .backgroundColor(Color.Black)
    .onAnimationStart((index: number, targetIndex: number, extraInfo: SwiperAnimationEvent) => {
      Logger.debug(TAG, `onAnimationStart index: ${index}, targetIndex: ${targetIndex}, extraInfo: ${extraInfo}.`);
      this.curIndex = targetIndex;
    })
    .onAnimationEnd((index: number, extraInfo: SwiperAnimationEvent) => {
      Logger.debug(TAG, `onAnimationEnd index: ${index}, extraInfo: ${extraInfo}.`);
    })
  }

  private reuseCallback(item: NodeItem): void {
    Logger.debug(TAG, `reuseCallback in, url:${item?.data?.url}`)
  }

  private recycleCallback(item: NodeItem): void {
    Logger.debug(TAG, `recycleCallback in, url:${item?.data?.url}`)
  }
}
```

---

## [37/100] ID: OH_0175 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-local-var-to-replace-state-var`
- Target File: `permissionmanager/src/main/ets/pages/application-tertiary.ets`
- Warning: Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
@Component
struct mediaDocumentPage {
  private backTitle: ResourceStr = (router.getParams() as RouterParams_3).backTitle;
  private permissions: Permissions[] = (router.getParams() as RouterParams_3).permission;
  private tokenId: number = (router.getParams() as RouterParams_3).tokenId;
  @State currentGroup: string = GlobalContext.load('currentPermissionGroup');
  @State folderStatus: boolean[] = GlobalContext.load('folderStatus');
  @State refresh: boolean = false;
  @State selected: number = 0; // Permission status array
  @State isRefreshReason: number = 0

  build() {
    Column() {
      GridRow({ gutter: Constants.GUTTER, columns: {
        xs: Constants.XS_COLUMNS, sm: Constants.SM_COLUMNS, md: Constants.MD_COLUMNS, lg: Constants.LG_COLUMNS } }) {
        GridCol({
          span: { xs: Constants.XS_SPAN, sm: Constants.SM_SPAN, md: Constants.MD_SPAN, lg: Constants.LG_SPAN },
          offset: { xs: Constants.XS_OFFSET, sm: Constants.SM_OFFSET, md: Constants.MD_OFFSET, lg: Constants.LG_OFFSET }
        }) {
          Row() {
            Column() {
              Row() {
                backBar({ title: JSON.stringify(this.backTitle), recordable: false })
              }
              Row() {
                Column() {
                  mediaDocumentItem({
                    selected: $selected, isRefreshReason: $isRefreshReason, folderStatus: $folderStatus
                  })
                }.width(Constants.FULL_WIDTH)
              }
              .margin({ top: Constants.TITLE_MARGIN_BOTTOM })
              .layoutWeight(Constants.LAYOUT_WEIGHT)
            }
          }
          .height(Constants.FULL_HEIGHT)
          .width(Constants.FULL_WIDTH)
          .backgroundColor($r('sys.color.ohos_id_color_sub_background'))
        }
      }.backgroundColor($r('sys.color.ohos_id_color_sub_background'))
    }
  }

  onPageShow() {
    console.log(TAG + 'onPageShow');
    if (this.refresh) {
      this.refreshStatus();
    }
    this.refresh = true;
  }

  refreshStatus() {
    if (reqPermissionInfo) {
      this.isRefreshReason ++;
    }
    console.log(TAG + 'Refresh permission status');
    let isGranted = true;
    let folderStatus = [false, false, false];
    if (
      this.currentGroup === 'LOCATION' &&
      !this.permissions.includes(FUZZY_LOCATION_PERMISSION) &&
      api >= Constants.API_VERSION_SUPPORT_STAGE
    ) {
      isGranted = false;
    }
    let atManager = abilityAccessCtrl.createAtManager();
    for (let i = 0; i < this.permissions.length; i++) {
      let permission = this.permissions[i];
      if (api >= Constants.API_VERSION_SUPPORT_STAGE && permission == PRECISE_LOCATION_PERMISSION) {
        continue;
      }
      if (permission == BACKGROUND_LOCATION_PERMISSION) {
        continue;
      }
      let res = atManager.verifyAccessTokenSync(this.tokenId, permission);
      if (res != abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED) {
        isGranted = false;
      }
      if (this.currentGroup === 'FOLDER' && res === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED) {
        switch (permission) {
          case DOWNLOAD_PERMISSION:
            folderStatus[0] = true;
            break;
          case DESKTOP_PERMISSION:
            folderStatus[1] = true;
            break;
          case DOCUMENTS_PERMISSION:
            folderStatus[2] = true;
            break;
        }
      }
    }
    console.log(TAG + 'isGranted: ' + JSON.stringify(isGranted));
    this.folderStatus = folderStatus;

    this.selected = isGranted ? Constants.PERMISSION_ALLOW : Constants.PERMISSION_BAN;
    if (this.currentGroup === 'PASTEBOARD') {
      try {
        let acManager = abilityAccessCtrl.createAtManager();
        acManager.getPermissionFlags(this.tokenId, PASTE).then(flag => {
          if (flag == Constants.PERMISSION_ALLOW_THIS_TIME) {
            this.selected = Constants.PERMISSION_ONLY_THIS_TIME;
          }
        })
      } catch (err) {
        console.log(TAG + 'getPermissionFlags error: ' + JSON.stringify(err));
      }
    }
    if (this.currentGroup === 'LOCATION') {
      this.selected = isGranted ? Constants.PERMISSION_ALLOWED_ONLY_DURING_USE : Constants.PERMISSION_BAN;
      let acManager = abilityAccessCtrl.createAtManager();
      let backgroundState = acManager.verifyAccessTokenSync(this.tokenId, BACKGROUND_LOCATION_PERMISSION);
      backgroundState === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED ?
        this.selected = Constants.PERMISSION_ALLOW : null;
    }
  }
}
```

---

## [38/100] ID: OH_0080 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- Target File: `entry/src/main/ets/pages/favorites/favoriteList.ets`
- Warning: Do not use stringify in the key generator function of LazyForEach

### Buggy Snippet
```typescript
@Component
struct FavoriteContent {
  @Link presenter: FavoriteListPresenter; //接受presenter（双向）
  @State mPresenter: FavoriteListPresenter = this.presenter;//收藏列表presenter
  isUsuallyShow: boolean = false;
  swipeActionCount: number = 0;// 滑动次数
  @State headAngle: number = 0;
  @State bodyAngle: number = 0;
  @State swipeScale: number = 1;
  @State endOffset: number = 0;// 滑动距离
  // 设备型号
  @StorageLink('breakpoint') curBp: string = 'sm';
  // 是否启动主题
  @StorageProp('isThemeActive') isThemeActive: boolean = false;
  // 是否启动无障碍
  @StorageProp(AccessibilityUtil.ISOPENACCESSIBILITY) isOpenAccessibility: boolean = false;//无障碍
  @StorageLink('hideIndexTitleTabBar') hideIndexTitleTabBar: boolean = false; //首页标题栏
  @StorageProp('isVerde') isVerde: boolean = false;
  private dustbinAnimationEnabled: boolean = true;//垃圾箱动画
  listScroller: ListScroller = new ListScroller();//列表滚动
  private isPC: boolean = EnvironmentProp.isPC();
  //---------------------------
  @State enterEndDeleteAreaString: string = "not enterEndDeleteArea"
  @State exitEndDeleteAreaString: string = "not exitEndDeleteArea"

  @Styles
  buttonStyle()
  {
    .borderRadius(20)
    .height($r('app.float.id_item_height_sm'))
    .width($r('app.float.id_item_height_sm'))
    .margin($r('app.float.id_card_margin_xl'))
  }

  aboutToDisappear(): void {
    HiLog.i(TAG, 'favoriteList aboutToDisappear!');
  }

//删除方法
  deleteAction(item: FavoriteListBean, index: number | undefined) {
    this.dustbinAnimationEnabled = false;//垃圾箱动画
    if (index === undefined) {//删除
      HiLog.i(TAG, 'deleteAction index is undefined')
      return;
    }
    let totalCount = this.presenter.favoriteDataSource.totalCount();//总数
    if (totalCount === 1) {
      // 只有一个联系人时，添加按钮
      AccessibilityUtil.getInstance().sendAccessibilityNotInterruptEvent(this.isOpenAccessibility, 'addFavoriteButton');
    } else {
    // 多个联系人时，删除按钮
      AccessibilityUtil.getInstance()
        .sendAccessibilityNotInterruptEvent(this.isOpenAccessibility, 'favorite' + (index + 1), 0);
    }

    animateTo({
      duration: 400,
      curve: Curve.Friction,
      onFinish: () => {
        this.dustbinAnimationEnabled = true;
      }
    }, () => {
      if (index !== undefined) {
        this.presenter.updateFavorite(0, Number(item.favorite.contactId), item);//
      }
    })
  }
  @Builder itemEnd(item: FavoriteListBean, index: number | undefined) {
    Row() {
      Button($r('app.string.accessibility_delete'))
        .margin("4vp")
        .onClick(()=>{
          this.deleteAction(item, index);
        })
    }
  }

  /**
   * FavoriteContent组件的构建方法
   * 使用响应式布局实现不同屏幕尺寸的适配
   */
  build() {
    // 使用GridRow实现响应式布局，根据屏幕尺寸设置不同的列数
    GridRow({ columns: { sm: 4, md: 8, lg: 12 }, gutter: { x: 12, y: 0 } }) {
      // GridCol设置为占据所有列宽，确保在不同屏幕尺寸下都能自适应
      GridCol({ span: { sm: 4, md: 8, lg: 12 } }) {
        // 列表组件，用于展示收藏联系人列表
        // space: 列表项间距为0
        // initialIndex: 初始显示第0项
        // scroller: 列表滚动控制器
        List({ space: 0, initialIndex: 0, scroller: this.listScroller }) {
          // 使用LazyForEach实现列表的懒加载，提高性能
          // favoriteDataSource: 收藏联系人数据源
          // item: 当前循环的收藏联系人数据
          // index: 当前项的索引
          LazyForEach(this.presenter.favoriteDataSource, (item: FavoriteListBean, index?: number | undefined) => {
            // 列表项组件，定义单个联系人的展示和交互
            ListItem(
              // customItemBuilder: this.favoriteListBuilder(item, index),
              //
              // swipeActionOptions: {//删除按钮
              //   deleteIconOptions: {//删除图标
              //     onAction: () => {//删除按钮点击事件
              //       this.deleteAction(item, index);//通过下标删除
              //     },
              //     iconOptions: {//删除图标属性
              //       accessibilityText: ResourceUtil.getStringByResource($r('app.string.accessibility_delete')) +
              //         ' ' + ResourceUtil.getStringByResource($r('app.string.accessibility_button'))//删除图标的辅助文本
              //     }
              //   },
              // 列表项的滑动删除
              //   fullDeleteOptions: {
              //     isFullDelete: true,//开启滑动超阈值自动删除
              //
              //     onFullDeleteAction: () => {
              //       animateTo({//删除动画
              //         duration: 350,
              //       }, () => {
              //         this.deleteAction(item, index); //通过下标删除
              //       })
              //     }
              //   }
              // }
            ) {
                // 调用列表项构建器，渲染联系人信息
                this.favoriteListBuilder(item, index)


            }
            // 配置列表项的滑动操作
            .swipeAction({
              // 配置列表项右侧滑动操作
              end:{
                // 滑动操作按钮构建器
                builder:()=>{
                  // 调用itemEnd方法构建删除和设置按钮
                  this.itemEnd(item, index)
                },
                // 滑动操作触发时的回调函数
                onAction:()=>{
                  // 使用animateTo实现动画效果
                  animateTo({
                    duration: 400, // 动画持续时间400ms
                  }, () => {
                    this.deleteAction(item, index);
                  })
                },

              }
            })

          }, (item: FavoriteListBean) => JSON.stringify(item))
        }

        // 配置列表的内容裁剪模式为安全区域
        .clipContent(ContentClipMode.SAFE_AREA)
        // 启用编辑模式
        .editMode(true)
        // 设置列表宽高为100%
        .width('100%')
        .height('100%')
        // 设置列表方向为垂直
        .listDirection(Axis.Vertical)
        // 设置边缘效果为弹性效果，并始终启用
        .edgeEffect(EdgeEffect.Spring, { alwaysEnabled: true })
        // 列表滚动事件回调
        .onDidScroll((scrollOffset: number, scrollState: ScrollState) => {
          // 当列表向下滚动时隐藏标题栏，向上滚动时显示标题栏
          if (scrollState === ScrollState.Scroll) {
            if (scrollOffset > 0 && !this.hideIndexTitleTabBar) {
              this.hideIndexTitleTabBar = true;
            } else if (scrollOffset < 0 && this.hideIndexTitleTabBar) {
              this.hideIndexTitleTabBar = false;
            }
          }
        })
        // 设置安全区域底部内边距为48vp
        .safeAreaPadding({ bottom: 48 })
      }
    }
    .flexShrink(1)
    // 设置左右内边距，根据设备类型和屏幕尺寸自适应
    .padding({
      left: this.isPC ? $r('sys.float.padding_level8') :
        this.curBp === 'lg' ? $r('sys.float.padding_level6') : 0,
      right: this.isPC ? $r('sys.float.padding_level8') :
        this.curBp === 'lg' ? $r('sys.float.padding_level12') : 0
    })
    // 可见区域变化事件回调
    .onVisibleAreaChange([0.0, 1.0], (isVisible: boolean, currentRatio: number) => {
      // 当组件完全可见时，增加滑动操作计数
      if (isVisible && currentRatio === 1) {
        this.swipeActionCount++;
      } 
      // 当组件完全不可见时，减少滑动操作计数
      else if (!isVisible && currentRatio === 0) {
        this.swipeActionCount--;
        // 当没有可见的滑动操作时，关闭所有滑动操作
        if (this.swipeActionCount <= 0) {
          this.swipeActionCount = 0;
          this.listScroller?.closeAllSwipeActions();
        }
      }
    })
    .height('100%')
    .width('100%')
  }

  /**
   * 收藏联系人列表项构建器
   * @param item 当前收藏联系人数据
   * @param index 当前项的索引
   */
  @Builder
  favoriteListBuilder(item: FavoriteListBean, index?: number | undefined) {

      // 列表项在顶层，可以滑动
      FavoriteListItem({ 
        presenter: $mPresenter, // 双向绑定的收藏列表presenter
        item: item, // 当前收藏联系人数据
        index: index // 当前项的索引
      })//列表项
        // 设置列表项的约束尺寸，根据设备类型设置不同的最小和最大高度
        .constraintSize({
          minHeight: this.isPC ? $r('app.float.id_item_height_large') : $r('app.float.id_item_height_max'),
          maxHeight: this.isPC ? $r('app.float.id_item_height_large') : $r('app.float.id_item_height_max')
        })
        // 设置zIndex确保列表项按照索引顺序显示
        .zIndex(index!)
  }

}
```

---

## [39/100] ID: OH_0111 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- Target File: `entry/src/main/ets/pages/dialer/callRecord/InterceptionCalls.ets`
- Warning: Do not use stringify in the key generator function of LazyForEach

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

---

## [40/100] ID: OH_0173 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-local-var-to-replace-state-var`
- Target File: `permissionmanager/src/main/ets/pages/dialogPlus.ets`
- Warning: Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
if (this.reqPerms.includes(PRECISE_LOCATION_PERMISSION)) {
          this.locationFlag = Constants.LOCATION_BOTH_PRECISE;
          let fuzzyIndex = this.reqPerms.indexOf(FUZZY_LOCATION_PERMISSION);
          if (stateGroup[fuzzyIndex] == Constants.PASS_OPER) {
            this.locationFlag = Constants.LOCATION_UPGRADE;
          }
        }
```

---

## [41/100] ID: OH_0195 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-reusable-component`
- Target File: `HMSliderPlayer/src/main/ets/components/HMSliderPlayer.ets`
- Warning: Use reusable components to define complex components whenever possible

### Buggy Snippet
```typescript
@Component
export struct HMSliderPlayer {
  @State curIndex: number = 0;
  @State foldStatus: number = 0;
  @State sheetData: SheetData = new SheetData();
  @State videoComponentOption: SliderPlayerSize = new SliderPlayerSize();
  private datasource: HMSliderPlayerIDataSource = new HMSliderPlayerIDataSource();
  private swiperController: SwiperController = new SwiperController();
  private hmAVPlayerMgr: HMAVPlayerMgr = new HMAVPlayerMgr();
  @Link hmSliderPlayerController: HMSliderPlayerController;
  private options?: HMSliderPlayerOptions;
  private windowMgr: WindowMgr = WindowMgr.getInstance();

  aboutToAppear(): void {
    this.hmSliderPlayerController?.set(this.hmAVPlayerMgr)
    this.hmSliderPlayerController?.set(this.videoComponentOption)
    WindowMgr.getInstance().setUIContext(this.getUIContext())
    window.getLastWindow(this.getUIContext().getHostContext(), (err: BusinessError, data) => {
      if (err.code) {
        Logger.error('Failed to obtain the top window. Code: ${public}d, message: ${public}s', err.code,
          err.message);
      }
      this.windowMgr.setWindowStage(data);
      this.windowMgr.registerOnWindowSizeChange((size: window.Size) => {

      })
    });
  }

  build() {
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
    .width(this.videoComponentOption.width)
    .height(this.videoComponentOption.height)
  }
}
```

---

## [42/100] ID: OH_0050 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-stringify-in-lazyforeach-key-generator`
- Target File: `entry/src/main/ets/pages/contacts/batchselectcontacts/SingleSelectContactPage.ets`
- Warning: Do not use stringify in the key generator function of LazyForEach

### Buggy Snippet
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

---

## [43/100] ID: OH_0184 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-local-var-to-replace-state-var`
- Target File: `permissionmanager/src/main/ets/pages/dialogPlus.ets`
- Warning: Replace state variables with local variables for temporary calculation

### Buggy Snippet
```typescript
if (this.reqPerms.includes(Permission.LOCATION)) {
        this.locationFlag = Constants.LOCATION_BOTH_PRECISE;
        let fuzzyIndex = this.reqPerms.indexOf(Permission.APPROXIMATELY_LOCATION);
        if (stateGroup[fuzzyIndex] == Constants.PASS_OPER) {
          this.locationFlag = Constants.LOCATION_UPGRADE;
        }
      }
```

---

## [44/100] ID: OH_0177 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-no-state-var-access-in-loop`
- Target File: `permissionmanager/src/main/ets/pages/authority-tertiary.ets`
- Warning: Avoid frequent state variable reads inside loop logic

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
              bundleInfo.language) // Get the first letter in the returned initials array
          );
          verifyAccessToken(bundleInfo.tokenId, this.list[0].permission).then(data => {
            // 0: have permission; -1: no permission
            if (data === Constants.PERMISSION_INDEX) {
              this.toggleIsOn[i] = true;
              this.isFirst[i] = true;
              this.permissionNum++;
            } else {
              this.toggleIsOn[i] = false;
              this.isFirst[i] = false;
            }
          })
          this.isRisk[i] = false;
          try {
            atManager.getPermissionFlags(bundleInfo.tokenId, this.list[0].permission).then(data => {
              if (data == Constants.PERMISSION_POLICY_FIXED) {
                this.isRisk[i] = true;
              }
            })
          } catch (err) {
            console.log(TAG + 'getPermissionFlags error: ' + JSON.stringify(err));
          }
        }
      })
```

---

## [45/100] ID: OH_0310 | ArkTS (T)
- Rule ID: `@previewer/mandatory-default-value-for-local-initialization`
- Target File: `HMRouterExamples/commons/ui_components/src/main/ets/components/CellGroupComponent.ets`
- Warning: If a component attribute supports local initialization, a valid, runtime-independent default value should be set for it.

### Buggy Snippet
```typescript
@Component
export struct CellGroup {
  private title: string | Resource | undefined;
  @BuilderParam closer: () => void;

  build() {
    Column() {
      if (this.title) {
        Text(this.title)
          .fontSize($r("app.float.font_lg"))
          .fontColor($r("app.color.text_secondary"))
          .fontWeight(FontWeight.Bold)
          .margin({ bottom: $r("app.float.vp_12"), top: $r("app.float.vp_16") })
          .alignSelf(ItemAlign.Start);
      }
      Column() {
        this.closer();
      }
      .width("100%")
      .clip(true)
      .borderRadius($r("app.float.vp_16"))
      .backgroundColor($r("app.color.color_white"));
    }.margin({ left: $r("app.float.vp_16"), right: $r("app.float.vp_16") });
  }
}
```

---

## [46/100] ID: OH_0136 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-object-link-to-replace-prop`
- Target File: `widescreen_uikit/src/main/ets/components/toolbarDialog/ToolbarDialog.ets`
- Warning: Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

### Buggy Snippet
```typescript
import Curves from '@ohos.curves';
import { KeyCode } from '@ohos.multimodalInput.keyCode';

const ITEM_WIDTH: number = 96;
const ITEM_HEIGHT: number = 96;
const TOOL_HEIGHT: number = 97;
const TOOL_BAR_PADDING: number = 24;
const TOOL_BAR_DX: number = 0;
const TOOL_BAR_DY: number = -64;
const ITEM_PADDING_TOP: number = 12;
const IMAGE_BACKBOARD: number = 40;
const IMAGE_SIZE: number = 24;
const TEXT_MARGIN_DEFAULT: number = 8;
const TEXT_MARGIN_CHANGE: number = 4;
const ITEM_PRESS_COLOR_BLENDS: Resource = $r("app.color.toolbarDialog_item_press_colorBlends");
const ITEM_HOVER_COLOR_BLENDS: Resource = $r("app.color.toolbarDialog_item_hover_colorBlends");
const ID_SUFFIX: string = getContext().resourceManager.getStringByNameSync('toolbardialog_id_suffix');

@CustomDialog
export struct ToolBarDialog {
  @Prop toolbarList: ToolBarOptions;
}
```

---

## [47/100] ID: OH_0023 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-reusable-component`
- Target File: `entry/src/main/ets/component/contactdetail/DetailCalllog.ets`
- Warning: Use reusable components to define complex components whenever possible

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

---

## [48/100] ID: OH_0374 | ArkTS (T)
- Rule ID: `@performance/foreach-args-check`
- Target File: `entry/src/main/ets/pages/example/EffectPage.ets`
- Warning: For performance purposes, set keyGenerator for ForEach.

### Buggy Snippet
```typescript
@Component
struct EffectPage {
  private controllers: LottieController[] = []
  private lottieViewPath: Resource[] = [
    $rawfile('common/lottie/data_base64.json'),
    $rawfile('common/rlottie/bell.json'),
    $rawfile('common/lottie/tint.json'),
    $rawfile('common/lottie/tri_tone.json'),
    $rawfile('common/lottie/stroke.json'),
  ]
  private lottieEffectNames: string[] = ["blur", "fill", "tint", "triTone", "stroke"]
  @State value :number = 1;
  build() {
    Column(){
      Text("Effect list").fontSize(20)
      Scroll() {
        Grid() {
          ForEach(this.lottieViewPath, (path: Resource, index) => {
            GridItem() {
              Column() {
                LottieView({
                  loop: true,
                  autoplay: true,
                  path: path,
                  controller: this.controllers[index],
                })
                  .width('90%')
                  .aspectRatio(1)
                  .backgroundColor('#F1F3F5')
                  .margin(10)
                  .onClick(()=>{
                    this.controllers[index].play()
                  })
                Text(this.lottieEffectNames[index])
                  .fontSize(14)
                  .margin({ top: 5, bottom: 5 })
                  .textAlign(TextAlign.Center)
                  .maxLines(2)
                  .textOverflow({ overflow: TextOverflow.Ellipsis })
              }
            }
          })
        }
        .columnsTemplate('1fr 1fr')
        .width('100%')
        .layoutWeight(1)
      }
      .scrollBar(BarState.Auto)
      .edgeEffect(EdgeEffect.Spring)
      .height('85%')
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
  aboutToAppear(): void {
    this.controllers = Array(this.lottieViewPath.length)
      .fill(null)
      .map(() => new LottieController())
  }
}
```

---

## [49/100] ID: OH_0236 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-use-object-link-to-replace-prop`
- Target File: `entry/src/main/ets/pages/conversation/MessageTypeTitleAndCalenderDate.ets`
- Warning: Use @ObjectLink instead of @Prop to reduce unnecessary deep copies

### Buggy Snippet
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

---

## [50/100] ID: OH_0275 | ArkTS (T)
- Rule ID: `@performance/hp-arkui-set-cache-count-for-lazyforeach-grid`
- Target File: `product/phone/src/main/ets/Setting/Volume/view/SystemRingToneComponent.ets`
- Warning: Set cachedCount to an appropriate value when using LazyForEach in grids

### Buggy Snippet
```typescript
Column() {
      List() {
        ListItemGroup() {
          // 振动设置项 UI
          if (VibratorUtil.isSupportVibrate()) {
            this.VibrateBuilder();
          }
          if (this.isShowCurrentRingtone) {
            this.CurrentRingtoneBuilder();
          }
          this.SelectRingtoneBuilder();
        }

        ListItem() {
          this.SelectBlankRingBuilder()
        }

        ListItemGroup() {
          LazyForEach(this.ringtoneList, (item: ToneAttrs, index: number) => {
            ListItem() {
              Column() {
                this.ringToneItem(item, index);
                if (index !== (this.ringtoneList?.ringtoneArray.length - 1)) {
                  Divider()
                    .height(px2vp(2))
                    .strokeWidth(0.5)
                    .color($r('sys.color.comp_divider'))
                    .lineCap(LineCapStyle.Square)
                    .padding({ left: $r('sys.float.padding_level4'), right: $r('sys.float.padding_level4') })
                    .width('100%')
                }
              }
              .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])
              .padding({
                top: index === 0 ? $r('sys.float.padding_level2') : 0,
                bottom: index === (this.ringtoneList?.ringtoneArray.length - 1) ? $r('sys.float.padding_level2') :
                  0,
                left: $r('sys.float.padding_level2'),
                right: $r('sys.float.padding_level2'),
              })
            }
          }, (item: ToneAttrs) => item?.title)
        }
        .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])
        .backgroundColor($r('sys.color.comp_background_list_card'))
        .borderRadius($r('sys.float.corner_radius_level10'))
      }
      .padding({
        left: DeviceUtil.isDevicePad() ? $r('sys.float.padding_level12') : $r('sys.float.padding_level8'),
        right: DeviceUtil.isDevicePad() ? $r('sys.float.padding_level12') : $r('sys.float.padding_level8'),
        bottom: 0,
      })
      .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])
      .width('100%')
      .height('100%')
    }
```

---

## [51/100] ID: CPP_0064 | C/C++ (T)
- Rule ID: `cppcheck/passedByValue`
- Target File: `ohos_jipp/entry/src/main/cpp/pdfiumwrapper/pdfium.cpp`
- Warning: Function parameter 'filename' should be passed by const reference.

### Buggy Snippet
```cpp
#include "aki/jsbind.h"
#include "pdfium.h"

Pdfium::Pdfium(std::string filename)
{
    FPDF_InitLibrary();
    doc = FPDF_LoadDocument(filename.c_str(), NULL);
    
    AKI_LOG(INFO) << "new Pdfium filename : " << filename << " doc = " << (void*)doc;
    return;
}
```

---

## [52/100] ID: CPP_0194 | C/C++ (T)
- Rule ID: `cppcheck/variableScope`
- Target File: `services/implementation/src/authentication_v2/dm_auth_message_processor.cpp`
- Warning: The scope of the variable 'isServiceIdExist' can be reduced.

### Buggy Snippet
```cpp
static void UpdateMatchAccessControlProfile(std::shared_ptr<DmAuthContext> context,
    DistributedDeviceProfile::AccessControlProfile &profile, bool &hasAcl, int64_t serviceId)
{
    LOGI("UpdateMatchAccessControlProfile start.");
    CHECK_NULL_VOID(context);
    JsonObject jsonObjServiceId(JsonCreateType::JSON_CREATE_TYPE_ARRAY);
    bool isServiceIdExist = false;
    std::string aceeSeviceId = profile.GetAccessee().GetAccesseeExtraData();
    JsonObject lastServiceId;
    if (!lastServiceId.Parse(aceeSeviceId)) {
        LOGE("Failed to parse JSON string");
        return;
    }
    if (lastServiceId.Contains(TAG_SERVICE_ID) && lastServiceId[TAG_SERVICE_ID].IsArray()) {
        auto tmpServiceId = lastServiceId[TAG_SERVICE_ID];
        for (auto& id : tmpServiceId.Items()) {
            int64_t idValue = id.Get<int64_t>();
            if (idValue != serviceId) {
                jsonObjServiceId.PushBack(idValue);
            } else {
                isServiceIdExist = true;
            }
        }
        if (!isServiceIdExist) {
            jsonObjServiceId.PushBack(serviceId);
        }
        lastServiceId.Insert(TAG_SERVICE_ID, jsonObjServiceId);
        DistributedDeviceProfile::Accessee accessee = profile.GetAccessee();
        accessee.SetAccesseeExtraData(lastServiceId.Dump());
        profile.SetAccessee(accessee);
        int32_t ret = DM_OK;
        ret = DistributedDeviceProfile::DistributedDeviceProfileClient::GetInstance().UpdateAccessControlProfile(
            profile);
        if (ret != DM_OK) {
            LOGE("UpdateAccessControlProfile failed.");
        } else {
            ServiceStateBindParameter bindParam = {context->accesser.tokenId, context->accesser.pkgName,
                DM_POINT_TO_POINT, context->accessee.deviceId, context->accessee.userId, serviceId};
            char deviceIdHash[DM_MAX_DEVICE_ID_LEN] = {0};
            Crypto::GetUdidHash(context->accessee.deviceId, reinterpret_cast<uint8_t *>(deviceIdHash));
            if (SoftbusCache::GetInstance().CheckIsOnline(std::string(deviceIdHash))) {
                context->listener->OnServiceStateOnlineResult(bindParam);
            }
        }
    } else {
        hasAcl = false;
    }
}
```

---

## [53/100] ID: CPP_0041 | C/C++ (T)
- Rule ID: `cppcheck/passedByValue`
- Target File: `ohos_YYEVA/library/src/main/cpp/bean/evaframeall.cpp`
- Warning: Function parameter 'datas' should be passed by const reference.

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

---

## [54/100] ID: CPP_0283 | C/C++ (T)
- Rule ID: `cppcheck/uninitvar`
- Target File: `components/nstackx/fillp/src/public/src/socket_common.c`
- Warning: Uninitialized variable: tableIndex

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

---

## [55/100] ID: CPP_0151 | C/C++ (T)
- Rule ID: `cppcheck/variableScope`
- Target File: `spinec/Spinec/src/main/cpp/thirdparty/spinec/spine/Skeleton.c`
- Warning: The scope of the variable 'child' can be reduced.

### Buggy Snippet
```cpp
static void _sortTransformConstraint(_spSkeleton *const internal, spTransformConstraint *constraint) {
	int i, boneCount;
	spBone **constrained;
	spBone *child;

	constraint->active = constraint->target->active && (!constraint->data->skinRequired || (internal->super.skin != 0 &&
																							spTransformConstraintDataArray_contains(
																									internal->super.skin->transformConstraints,
																									constraint->data)));
	if (!constraint->active) return;

	_sortBone(internal, constraint->target);

	constrained = constraint->bones;
	boneCount = constraint->bonesCount;
	if (constraint->data->local) {
		for (i = 0; i < boneCount; i++) {
			child = constrained[i];
			_sortBone(internal, child->parent);
			_sortBone(internal, child);
		}
	} else {
		for (i = 0; i < boneCount; i++)
			_sortBone(internal, constrained[i]);
	}

	_addToUpdateCache(internal, SP_UPDATE_TRANSFORM_CONSTRAINT, constraint);

	for (i = 0; i < boneCount; i++)
		_sortReset(constrained[i]->children, constrained[i]->childrenCount);
	for (i = 0; i < boneCount; i++)
		constrained[i]->sorted = 1;
}
```

---

## [56/100] ID: CPP_0322 | C/C++ (T)
- Rule ID: `cppcheck/identicalInnerCondition`
- Target File: `frameworks/js/src/thumbnail_manager.cpp`
- Warning: Identical inner 'if' condition is always true.

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

---

## [57/100] ID: CPP_0317 | C/C++ (T)
- Rule ID: `cppcheck/stlIfStrFind`
- Target File: `frameworks/innerkitsimpl/medialibrary_data_extension/src/operation/photo_owner_album_id_operation.cpp`
- Warning: Inefficient usage of string::find() in condition; string::starts_with() could be faster.

### Buggy Snippet
```cpp
/**
 * @brief Build MediaData from lPath.
 */
MediaData PhotoOwnerAlbumIdOperation::BuildAlbumInfoByLPath(const std::string &lPath)
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

---

## [58/100] ID: CPP_0186 | C/C++ (T)
- Rule ID: `cppcheck/useStlAlgorithm`
- Target File: `interfaces/kits/js4.0/src/dm_native_util.cpp`
- Warning: Consider using std::find_if algorithm instead of a raw loop.

### Buggy Snippet
```cpp
std::string GetDeviceTypeById(DmDeviceType type)
{
    const static std::pair<DmDeviceType, std::string> mapArray[] = {
        {DEVICE_TYPE_UNKNOWN, DEVICE_TYPE_UNKNOWN_STRING},
        {DEVICE_TYPE_PHONE, DEVICE_TYPE_PHONE_STRING},
        {DEVICE_TYPE_PAD, DEVICE_TYPE_PAD_STRING},
        {DEVICE_TYPE_TV, DEVICE_TYPE_TV_STRING},
        {DEVICE_TYPE_CAR, DEVICE_TYPE_CAR_STRING},
        {DEVICE_TYPE_WATCH, DEVICE_TYPE_WATCH_STRING},
        {DEVICE_TYPE_WIFI_CAMERA, DEVICE_TYPE_WIFICAMERA_STRING},
        {DEVICE_TYPE_PC, DEVICE_TYPE_PC_STRING},
        {DEVICE_TYPE_SMART_DISPLAY, DEVICE_TYPE_SMART_DISPLAY_STRING},
        {DEVICE_TYPE_2IN1, DEVICE_TYPE_2IN1_STRING},
        {DEVICE_TYPE_GLASSES, DEVICE_TYPE_GLASSES_STRING},
    };
    for (const auto& item : mapArray) {
        if (item.first == type) {
            return item.second;
        }
    }
    return DEVICE_TYPE_UNKNOWN_STRING;
}
```

---

## [59/100] ID: CPP_0296 | C/C++ (T)
- Rule ID: `cppcheck/noExplicitConstructor`
- Target File: `core/connection/wifi_direct_cpp/event/wifi_direct_event_dispatcher.h`
- Warning: Struct 'ProcessorTerminate' has a constructor with 1 argument that is not explicit.

### Buggy Snippet
```cpp
struct ProcessorTerminate : public std::exception {
    ProcessorTerminate(ProcessorTerminateReason reason = ProcessorTerminateReason::SUCCESS) : reason_(reason) {}
    ProcessorTerminateReason reason_;
};
```

---

## [60/100] ID: CPP_0099 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `ohos_smack/library/src/main/cpp/Smack.cpp`
- Warning: Condition 'data==nullptr' is always false

### Buggy Snippet
```cpp
bool Smack::handleSubscriptionRequest(const JID &jid, const std::string &msg)
{
    LOGI("smack handleSubscriptionRequest jid:%s msg:%s  %d", jid.full().c_str(), msg.c_str(), __LINE__);

    if (tsfn_sub == nullptr) {
        return true;
    }

    std::string resultStr = "";
    resultStr.append("{");
    resultStr.append("\"jid\":");
    resultStr.append("\"");
    resultStr.append(jid.bare().c_str());
    resultStr.append("\"");
    resultStr.append(",\"name\":");
    resultStr.append("\"");
    resultStr.append(jid.username().c_str());
    resultStr.append("\"");
    resultStr.append(",\"msg\":");
    resultStr.append("\"");
    resultStr.append(msg.c_str());
    resultStr.append("\"");
    resultStr.append("}");
    ThreadSafeInfoSub *data = &g_threadInfoSub;
    if (data == nullptr) {
        LOGE("SMACK_TAG---------> [Smack.handleSubscriptionRequest]data is null");
        return false;
    }
    data->result = resultStr.c_str();
    napi_acquire_threadsafe_function(tsfn_sub);
    // 调用主线程函数，传入 Data
    napi_call_threadsafe_function(tsfn_sub, data, napi_tsfn_blocking);
    return true;
}
```

---

## [61/100] ID: CPP_0036 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `XLog/library/src/main/cpp/ohos_utils/napi_handler.cpp`
- Warning: Condition 'buf.get()==nullptr' is always false

### Buggy Snippet
```cpp
template <>
std::string NapiHandler::ParseArg<std::string>(const napi_value &arg) const
{
    std::string result = "";
    size_t length = 0;

    NapiCall(env_, napi_get_value_string_utf8(env_, arg, nullptr, 0, &length));
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
    NapiCall(env_, napi_get_value_string_utf8(env_, arg, buf.get(), length + 1, &length));
    result = buf.get();
    return result;
}
```

---

## [62/100] ID: CPP_0024 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `napi/settings/napi_settings.cpp`
- Warning: Condition 'asyncCallbackInfo!=nullptr' is always true

### Buggy Snippet
```cpp
napi_value napi_set_value_sync_ext(bool stageMode, size_t argc, napi_env env, napi_value *args)
{
    AsyncCallbackInfo *asyncCallbackInfo = new AsyncCallbackInfo();
    if (asyncCallbackInfo == nullptr) {
        SETTING_LOG_ERROR("asyncCallbackInfo is null");
        return wrap_void_to_js(env);
    }
    asyncCallbackInfo->key = unwrap_string_from_js(env, args[PARAM1], false);
    napi_valuetype valueType;

    // define table name
    if (argc == ARGS_FOUR) {
        if (napi_typeof(env, args[PARAM3], &valueType) != napi_ok) {
            SETTING_LOG_ERROR("napi_typeof error");
            if (asyncCallbackInfo != nullptr) {
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
            }
            return wrap_void_to_js(env);
        }
        if (valueType != napi_string) {
            SETTING_LOG_ERROR("tableName IS NOT STRING");
            delete asyncCallbackInfo;
            asyncCallbackInfo = nullptr;
            return wrap_void_to_js(env);
        } else {
            asyncCallbackInfo->tableName = unwrap_string_from_js(env, args[PARAM3]);
            if (IsTableNameInvalid(asyncCallbackInfo->tableName)) {
                SETTING_LOG_ERROR("INVALID tableName");
                delete asyncCallbackInfo;
                asyncCallbackInfo = nullptr;
                return wrap_void_to_js(env);
            }
        }
    } else {
        asyncCallbackInfo->tableName = "global";
    }
    auto contextS = OHOS::AbilityRuntime::GetStageModeContext(env, args[PARAM0]);
    if (contextS == nullptr) {
        SETTING_LOG_ERROR("get context is error.");
        asyncCallbackInfo->status = STATUS_ERROR_CODE;
    } else {
        asyncCallbackInfo->token = contextS->GetToken();
        SetValueExecuteExt(env, (void *)asyncCallbackInfo, unwrap_string_from_js(env, args[PARAM2],
            true, true));
    }
    napi_value result = wrap_bool_to_js(env, ThrowError(env, asyncCallbackInfo->status));
    delete asyncCallbackInfo;
    asyncCallbackInfo = nullptr;
    return result;
}
```

---

## [63/100] ID: CPP_0339 | C/C++ (T)
- Rule ID: `cppcheck/identicalInnerCondition`
- Target File: `services/media_mtp/src/mtp_medialibrary_manager.cpp`
- Warning: Identical inner 'if' condition is always true.

### Buggy Snippet
```cpp
std::shared_ptr<MtpMedialibraryManager> MtpMedialibraryManager::GetInstance()
{
    if (instance_ == nullptr) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (instance_ == nullptr) {
            instance_ = std::make_shared<MtpMedialibraryManager>();
        }
    }
    return instance_;
}
```

---

## [64/100] ID: CPP_0117 | C/C++ (T)
- Rule ID: `cppcheck/redundantAssignment`
- Target File: `ohos_vlc/library/src/main/cpp/napi_init.cpp`
- Warning: Variable 'status' is reassigned a value before the old one has been used.

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

---

## [65/100] ID: CPP_0149 | C/C++ (T)
- Rule ID: `cppcheck/variableScope`
- Target File: `spinec/Spinec/src/main/cpp/thirdparty/spinec/spine/IkConstraint.c`
- Warning: The scope of the variable 'sa' can be reduced.

### Buggy Snippet
```cpp
void spIkConstraint_apply1(spBone *bone, float targetX, float targetY, int /*boolean*/ compress, int /*boolean*/ stretch,
						   int /*boolean*/ uniform, float alpha) {
	spBone *p = bone->parent;
	float pa = p->a, pb = p->b, pc = p->c, pd = p->d;
	float rotationIK = -bone->ashearX - bone->arotation;
	float tx = 0, ty = 0, sx = 0, sy = 0, s = 0, sa = 0, sc = 0;

	switch (bone->data->inherit) {
		case SP_INHERIT_ONLYTRANSLATION:
			tx = (targetX - bone->worldX) * SIGNUM(bone->skeleton->scaleX);
			ty = (targetY - bone->worldY) * SIGNUM(bone->skeleton->scaleY);
			break;
		case SP_INHERIT_NOROTATIONORREFLECTION: {
			s = ABS(pa * pd - pb * pc) / MAX(0.0001f, pa * pa + pc * pc);
			sa = pa / bone->skeleton->scaleX;
			sc = pc / bone->skeleton->scaleY;
			pb = -sc * s * bone->skeleton->scaleX;
			pd = sa * s * bone->skeleton->scaleY;
			rotationIK += ATAN2(sc, sa) * RAD_DEG;
		}// fallthrough
		default: {
			float x = targetX - p->worldX, y = targetY - p->worldY;
			float d = pa * pd - pb * pc;
			if (ABS(d) <= 0.0001f) {
				tx = 0;
				ty = 0;
			} else {
				tx = (x * pd - y * pb) / d - bone->ax;
				ty = (y * pa - x * pc) / d - bone->ay;
			}
		}
	}
	rotationIK += ATAN2(ty, tx) * RAD_DEG;

	if (bone->ascaleX < 0) rotationIK += 180;
	if (rotationIK > 180) rotationIK -= 360;
	else if (rotationIK < -180)
		rotationIK += 360;
	sx = bone->ascaleX;
	sy = bone->ascaleY;
	if (compress || stretch) {
		float b, dd;
		switch (bone->data->inherit) {
			case SP_INHERIT_NOSCALE:
			case SP_INHERIT_NOSCALEORREFLECTION:
				tx = targetX - bone->worldX;
				ty = targetY - bone->worldY;
			default:;
		}
		b = bone->data->length * sx, dd = SQRT(tx * tx + ty * ty);
		if ((compress && dd < b) || ((stretch && dd > b) && (b > 0.0001f))) {
			s = (dd / b - 1) * alpha + 1;
			sx *= s;
			if (uniform) sy *= s;
		}
	}
	spBone_updateWorldTransformWith(bone, bone->ax, bone->ay, bone->arotation + rotationIK * alpha, sx,
									sy, bone->ashearX, bone->ashearY);
}
```

---

## [66/100] ID: CPP_0120 | C/C++ (T)
- Rule ID: `cppcheck/shadowVariable`
- Target File: `socketio/library/src/main/cpp/client_socket.h`
- Warning: Local variable 'result' shadows outer variable

### Buggy Snippet
```cpp
void CallJsAckBinary(napi_env env, napi_value jsCb, void *context, void *data)
{
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> 0 CallJsEmit ");
    napi_value undefined;
    napi_status undefinedStatus = napi_get_undefined(env, &undefined);
    if (undefinedStatus != napi_ok) {
        return;
    }
    napi_value ret;
    
    // 解析参数 data
    std::unique_ptr<BinaryInfo> arg(static_cast<BinaryInfo*>(data));
    if (arg == nullptr) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "[CallJsBinary]BinaryInfo is null");
        return;
    }
    size_t length = arg->result.size();
    
    void *nativePtr = nullptr;
    // 创建一个新的 ArrayBuffer，长度等于字符串的长度
    napi_value arrayBuffer;
    napi_create_arraybuffer(env, length, &nativePtr, &arrayBuffer);
    if (memcpy_s(nativePtr, length, arg->result.data(), length) != EOK) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, "socket.io-client-cpp", "[CallJsAckBinary]memcpy_s is error");
        return;
    }

    napi_typedarray_type arrayType = static_cast<napi_typedarray_type>(napi_uint8_array);
    
    napi_value typedArray = nullptr;
    napi_create_typedarray(env, arrayType, length, arrayBuffer, 0, &typedArray);
    
    napi_value requestCode = nullptr;
    napi_create_int32(env, arg->code, &requestCode);

    napi_value result[] = {nullptr, nullptr};
    result[0] = requestCode;
    result[1] = typedArray;
    
    // 调用 js 回调函数
    napi_status status = napi_call_function(env, undefined, jsCb, 2, result, &ret);
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, "SOCKETIO_TAG------> 2 CallJsBinary %{public}d", status);
}
```

---

## [67/100] ID: CPP_0052 | C/C++ (T)
- Rule ID: `cppcheck/noExplicitConstructor`
- Target File: `ohos_YYEVA/library/src/main/cpp/ohos/napi_async_handler.h`
- Warning: Class 'NapiScope' has a constructor with 1 argument that is not explicit.

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

---

## [68/100] ID: CPP_0195 | C/C++ (T)
- Rule ID: `cppcheck/useStlAlgorithm`
- Target File: `services/implementation/src/authentication_v2/dm_auth_message_processor.cpp`
- Warning: Consider using std::any_of algorithm instead of a raw loop.

### Buggy Snippet
```cpp
bool DmAuthMessageProcessor::IsExistTheToken(JsonObject &proxyObj, int64_t tokenId)
{
    if (proxyObj.IsDiscarded()) {
        return false;
    }
    for (auto const &item : proxyObj.Items()) {
        if (item.IsDiscarded() || !item.IsNumberInteger()) {
            continue;
        }
        if (tokenId == item.Get<int64_t>()) {
            return true;
        }
    }
    return false;
}
```

---

## [69/100] ID: CPP_0143 | C/C++ (T)
- Rule ID: `cppcheck/variableScope`
- Target File: `spinec/Spinec/src/main/cpp/thirdparty/stb/stb_image.h`
- Warning: The scope of the variable 'len' can be reduced.

### Buggy Snippet
```cpp
static int stbi__psd_decode_rle(stbi__context *s, stbi_uc *p, int pixelCount)
{
   int count, nleft, len;

   count = 0;
   while ((nleft = pixelCount - count) > 0) {
      len = stbi__get8(s);
      if (len == 128) {
      } else if (len < 128) {
         len++;
         if (len > nleft) return 0; // corrupt data
         count += len;
         while (len) {
            *p = stbi__get8(s);
            p += 4;
            len--;
         }
      } else if (len > 128) {
         stbi_uc   val;
         len = 257 - len;
         if (len > nleft) return 0; // corrupt data
         val = stbi__get8(s);
         count += len;
         while (len) {
            *p = val;
            p += 4;
            len--;
         }
      }
   }

   return 1;
}
```

---

## [70/100] ID: CPP_0233 | C/C++ (T)
- Rule ID: `cppcheck/nullPointer`
- Target File: `adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c`
- Warning: Possible null pointer dereference: it

### Buggy Snippet
```cpp
static ServerConnection *GetServerConnectionByConnIdUnsafe(int32_t connId)
{
    ServerConnection *it = NULL;
    ServerConnection *target = NULL;
    LIST_FOR_EACH_ENTRY(it, &g_softBusGattsManager.connections, ServerConnection, node) {
        if (it->connId == connId) {
            target = it;
            break;
        }
    }
    return target;
}
```

---

## [71/100] ID: CPP_0326 | C/C++ (T)
- Rule ID: `cppcheck/stlIfStrFind`
- Target File: `services/media_analysis_data_manager/src/dao/medialibrary_smartalbum_map_operations.cpp`
- Warning: Inefficient usage of string::find() in condition; string::starts_with() could be faster.

### Buggy Snippet
```cpp
static string GetNewPath(const string &path, const string &srcRelPath, const string &newRelPath)
{
    if ((path.find(srcRelPath) != 0) && (path.find(ROOT_MEDIA_DIR + srcRelPath) != 0)) {
        return "";
    }
    string newPath = newRelPath;
    if (path.find(ROOT_MEDIA_DIR) != string::npos) {
        newPath = ROOT_MEDIA_DIR + newPath;
    }
    newPath += path.substr(path.find(srcRelPath) + srcRelPath.length());
    return newPath;
}
```

---

## [72/100] ID: CPP_0187 | C/C++ (T)
- Rule ID: `cppcheck/useStlAlgorithm`
- Target File: `interfaces/kits/taihe/src/ani_dm_utils.cpp`
- Warning: Consider using std::find_if algorithm instead of a raw loop.

### Buggy Snippet
```cpp
std::string GetDeviceTypeById(const DmDeviceType &type)
{
    const static std::pair<DmDeviceType, std::string> mapArray[] = {
        {DEVICE_TYPE_UNKNOWN, DEVICE_TYPE_UNKNOWN_STRING},
        {DEVICE_TYPE_PHONE, DEVICE_TYPE_PHONE_STRING},
        {DEVICE_TYPE_PAD, DEVICE_TYPE_PAD_STRING},
        {DEVICE_TYPE_TV, DEVICE_TYPE_TV_STRING},
        {DEVICE_TYPE_CAR, DEVICE_TYPE_CAR_STRING},
        {DEVICE_TYPE_WATCH, DEVICE_TYPE_WATCH_STRING},
        {DEVICE_TYPE_WIFI_CAMERA, DEVICE_TYPE_WIFICAMERA_STRING},
        {DEVICE_TYPE_PC, DEVICE_TYPE_PC_STRING},
        {DEVICE_TYPE_SMART_DISPLAY, DEVICE_TYPE_SMART_DISPLAY_STRING},
        {DEVICE_TYPE_2IN1, DEVICE_TYPE_2IN1_STRING},
    };
    for (const auto &item : mapArray) {
        if (item.first == type) {
            return item.second;
        }
    }
    return DEVICE_TYPE_UNKNOWN_STRING;
}
```

---

## [73/100] ID: CPP_0084 | C/C++ (T)
- Rule ID: `cppcheck/passedByValue`
- Target File: `ohos_luaarkts/luaarkts/src/main/cpp/napi_arkts.cpp`
- Warning: Function parameter 'strTableName' should be passed by const reference.

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

---

## [74/100] ID: CPP_0190 | C/C++ (T)
- Rule ID: `cppcheck/useStlAlgorithm`
- Target File: `services/implementation/src/authentication_v2/auth_stages/auth_confirm.cpp`
- Warning: Consider using std::any_of algorithm instead of a raw loop.

### Buggy Snippet
```cpp
bool AuthSinkConfirmState::IsUserAuthorizeProxy(JsonObject &paramObj, std::shared_ptr<DmAuthContext> context)
{
    if (paramObj.IsDiscarded()) {
        return false;
    }
    for (auto const &item : paramObj.Items()) {
        if (context->accessee.serviceId == std::stoll(item[TAG_SERVICE_ID].Get<std::string>())) {
            return true;
        }
    }
    return false;
}
```

---

## [75/100] ID: CPP_0182 | C/C++ (T)
- Rule ID: `cppcheck/useStlAlgorithm`
- Target File: `commondependency/src/deviceprofile_connector.cpp`
- Warning: Consider using std::any_of algorithm instead of a raw loop.

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

---

## [76/100] ID: CPP_0108 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `ohos_smack/library/src/main/cpp/room.cpp`
- Warning: Condition 'data==nullptr' is always false

### Buggy Snippet
```cpp
void room::handleMUCInfo(MUCRoom * /* room */, int features, const std::string &name, const DataForm *infoForm)
{
    if (infoForm == nullptr) {
        LOGE("SMACK_TAG---------> [room.handleMUCInfo]infoForm is null");
        return;
    }
    // todo 房间信息获取
    LOGD("handleMUCInfo features: %d, name: %s, form xml: %s\n",
        features, name.c_str(), infoForm->tag()->xml().c_str());

    ThreadSafeRoomInfo *data = &g_threadRoomInfo;
    if (data == nullptr) {
        LOGE("SMACK_TAG---------> [room.handleMUCMessage]data is null");
        return;
    }
    data->roomInfo = infoForm->tag()->xml().c_str();
    NapiJsCallBack(data);
}
```

---

## [77/100] ID: CPP_0344 | C/C++ (T)
- Rule ID: `cppcheck/functionStatic`
- Target File: `NativeAPI/FunctionFlowRuntime/entry/src/main/cpp/sort_class.cpp`
- Warning: Technically the member function 'ParallelBucketSort::ParallelSortBucket' can be static (but you may consider moving to unnamed namespace).

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

---

## [78/100] ID: CPP_0137 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `spinec/Spinec/src/main/cpp/thirdparty/stb/stb_image.h`
- Warning: Condition '!easy' is always true

### Buggy Snippet
```cpp
if (info.bpp < 16) {
      int z=0;
      if (psize == 0 || psize > 256) { STBI_FREE(out); return stbi__errpuc("invalid", "Corrupt BMP"); }
      for (i=0; i < psize; ++i) {
         pal[i][2] = stbi__get8(s);
         pal[i][1] = stbi__get8(s);
         pal[i][0] = stbi__get8(s);
         if (info.hsz != 12) stbi__get8(s);
         pal[i][3] = 255;
      }
      stbi__skip(s, info.offset - info.extra_read - info.hsz - psize * (info.hsz == 12 ? 3 : 4));
      if (info.bpp == 1) width = (s->img_x + 7) >> 3;
      else if (info.bpp == 4) width = (s->img_x + 1) >> 1;
      else if (info.bpp == 8) width = s->img_x;
      else { STBI_FREE(out); return stbi__errpuc("bad bpp", "Corrupt BMP"); }
      pad = (-width)&3;
      if (info.bpp == 1) {
         for (j=0; j < (int) s->img_y; ++j) {
            int bit_offset = 7, v = stbi__get8(s);
            for (i=0; i < (int) s->img_x; ++i) {
               int color = (v>>bit_offset)&0x1;
               out[z++] = pal[color][0];
               out[z++] = pal[color][1];
               out[z++] = pal[color][2];
               if (target == 4) out[z++] = 255;
               if (i+1 == (int) s->img_x) break;
               if((--bit_offset) < 0) {
                  bit_offset = 7;
                  v = stbi__get8(s);
               }
            }
            stbi__skip(s, pad);
         }
      } else {
         for (j=0; j < (int) s->img_y; ++j) {
            for (i=0; i < (int) s->img_x; i += 2) {
               int v=stbi__get8(s),v2=0;
               if (info.bpp == 4) {
                  v2 = v & 15;
                  v >>= 4;
               }
               out[z++] = pal[v][0];
               out[z++] = pal[v][1];
               out[z++] = pal[v][2];
               if (target == 4) out[z++] = 255;
               if (i+1 == (int) s->img_x) break;
               v = (info.bpp == 8) ? stbi__get8(s) : v2;
               out[z++] = pal[v][0];
               out[z++] = pal[v][1];
               out[z++] = pal[v][2];
               if (target == 4) out[z++] = 255;
            }
            stbi__skip(s, pad);
         }
      }
   } else {
      int rshift=0,gshift=0,bshift=0,ashift=0,rcount=0,gcount=0,bcount=0,acount=0;
      int z = 0;
      int easy=0;
      stbi__skip(s, info.offset - info.extra_read - info.hsz);
      if (info.bpp == 24) width = 3 * s->img_x;
      else if (info.bpp == 16) width = 2*s->img_x;
      else /* bpp = 32 and pad = 0 */ width=0;
      pad = (-width) & 3;
      if (info.bpp == 24) {
         easy = 1;
      } else if (info.bpp == 32) {
         if (mb == 0xff && mg == 0xff00 && mr == 0x00ff0000 && ma == 0xff000000)
            easy = 2;
      }
      if (!easy) {
         if (!mr || !mg || !mb) { STBI_FREE(out); return stbi__errpuc("bad masks", "Corrupt BMP"); }
         rshift = stbi__high_bit(mr)-7; rcount = stbi__bitcount(mr);
         gshift = stbi__high_bit(mg)-7; gcount = stbi__bitcount(mg);
         bshift = stbi__high_bit(mb)-7; bcount = stbi__bitcount(mb);
         ashift = stbi__high_bit(ma)-7; acount = stbi__bitcount(ma);
         if (rcount > 8 || gcount > 8 || bcount > 8 || acount > 8) { STBI_FREE(out); return stbi__errpuc("bad masks", "Corrupt BMP"); }
      }
      for (j=0; j < (int) s->img_y; ++j) {
         if (easy) {
            for (i=0; i < (int) s->img_x; ++i) {
               unsigned char a;
               out[z+2] = stbi__get8(s);
               out[z+1] = stbi__get8(s);
               out[z+0] = stbi__get8(s);
               z += 3;
               a = (easy == 2 ? stbi__get8(s) : 255);
               all_a |= a;
               if (target == 4) out[z++] = a;
            }
         } else {
            int bpp = info.bpp;
            for (i=0; i < (int) s->img_x; ++i) {
               stbi__uint32 v = (bpp == 16 ? (stbi__uint32) stbi__get16le(s) : stbi__get32le(s));
               unsigned int a;
               out[z++] = STBI__BYTECAST(stbi__shiftsigned(v & mr, rshift, rcount));
               out[z++] = STBI__BYTECAST(stbi__shiftsigned(v & mg, gshift, gcount));
               out[z++] = STBI__BYTECAST(stbi__shiftsigned(v & mb, bshift, bcount));
               a = (ma ? stbi__shiftsigned(v & ma, ashift, acount) : 255);
               all_a |= a;
               if (target == 4) out[z++] = STBI__BYTECAST(a);
            }
         }
         stbi__skip(s, pad);
      }
   }

   if (target == 4 && all_a == 0)
      for (i=4*s->img_x*s->img_y-1; i >= 0; i -= 4)
         out[i] = 255;

   if (flip_vertically) {
      stbi_uc t;
      for (j=0; j < (int) s->img_y>>1; ++j) {
         stbi_uc *p1 = out +      j     *s->img_x*target;
         stbi_uc *p2 = out + (s->img_y-1-j)*s->img_x*target;
         for (i=0; i < (int) s->img_x*target; ++i) {
            t = p1[i]; p1[i] = p2[i]; p2[i] = t;
         }
      }
   }

   if (req_comp && req_comp != target) {
      out = stbi__convert_format(out, target, req_comp, s->img_x, s->img_y);
      if (out == NULL) return out; // stbi__convert_format frees input on failure
   }

   *x = s->img_x;
   *y = s->img_y;
   if (comp) *comp = s->img_n;
   return out;
}
```

---

## [79/100] ID: CPP_0350 | C/C++ (T)
- Rule ID: `cppcheck/uninitvar`
- Target File: `library/src/main/cpp/napi/http2_common.h`
- Warning: Uninitialized variable: handleIoResult.isRecv

### Buggy Snippet
```cpp
HandleIoResult HandleIo(Connection *connection, string reqId)
{
    LOGE("HandleIo session %p reqId %s", connection->session, reqId.c_str());
    HandleIoResult handleIoResult;
    if (!connection->session || IsDestroyed(reqId)) {
        handleIoResult.code = -1;
        return handleIoResult;
    }
    int sessionResult = 0;
    sessionResult = nghttp2_session_recv(connection->session);
    if (sessionResult != 0) {
        LOGE("nghttp2_session_recv %d reqId %s ", sessionResult, reqId.c_str());
        handleIoResult.code = sessionResult;
        handleIoResult.isRecv = true;
        return handleIoResult;
    }
    sessionResult = nghttp2_session_send(connection->session);
    if (sessionResult != 0) {
        LOGE("nghttp2_session_send %d reqId %s", sessionResult, reqId.c_str());
        handleIoResult.code = sessionResult;
        handleIoResult.isRecv = false;
        return handleIoResult;
    }
    LOGE("HandleIo session end sessionResult %d reqId %s sessionResult %d",
        sessionResult, reqId.c_str(), sessionResult);
    handleIoResult.code = sessionResult;
    return handleIoResult;
}
```

---

## [80/100] ID: CPP_0332 | C/C++ (T)
- Rule ID: `cppcheck/identicalInnerCondition`
- Target File: `services/media_cloud_enhancement/src/enhancement_manager.cpp`
- Warning: Identical inner 'if' condition is always true.

### Buggy Snippet
```cpp
bool EnhancementManager::LoadService()
{
#ifdef ABILITY_CLOUD_ENHANCEMENT_SUPPORT
    if (enhancementService_ == nullptr) {
        unique_lock<mutex> lock(mutex_);
        if (enhancementService_ == nullptr) {
            enhancementService_ = make_shared<EnhancementServiceAdapter>();
        }
    }
    if (enhancementService_ == nullptr) {
        return false;
    }
    return true;
#else
    return false;
#endif
}
```

---

## [81/100] ID: CPP_0037 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `ohos_7zip/library/src/main/cpp/uncompress/uncompress.cpp`
- Warning: Condition 'i<offset' is always true

### Buggy Snippet
```cpp
for (int i = 0; i < bits; i++) {
        int j = dis(generate);
        tmp += (i < offset) ? ('0' + j) : ('a' + j - offset);
    }
    tmp += ".ohos";
    return tmp;
}
```

---

## [82/100] ID: CPP_0312 | C/C++ (T)
- Rule ID: `cppcheck/stlIfStrFind`
- Target File: `frameworks/innerkitsimpl/medialibrary_data_extension/src/medialibrary_object_utils.cpp`
- Warning: Inefficient usage of string::find() in condition; string::starts_with() could be faster.

### Buggy Snippet
```cpp
static string GetRelativePathFromPath(const string &path)
{
    string relativePath;
    if (path.find(ROOT_MEDIA_DIR) == 0) {
        relativePath = path.substr(ROOT_MEDIA_DIR.length());
    }
    auto pos = relativePath.rfind('/');
    if (pos == string::npos) {
        return "";
    }
    return relativePath.substr(0, pos + 1);
}
```

---

## [83/100] ID: CPP_0088 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `ohos_minizip/library/src/main/cpp/minizipAdapter/minizipCompressNative.cpp`
- Warning: Condition 'zipFilePath_.empty()' is always true

### Buggy Snippet
```cpp
int32_t MinizipCompressNative::Create()
{
    if(!zipFilePath_.empty()){
        isDiskCompress_ = true;
    }
    else if (zipFilePath_.empty() && !catchPath_.empty()) {
        isDiskCompress_ = false;
    }
    else{
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOGNAME_COM,
            "zipFilePath_ and catchPath_ is empty\n");
        return CompressError::CompressPathIsNull;
    }

    if(zipWriter_) {
        OH_LOG_Print(LOG_APP, LOG_WARN, LOG_DOMAIN, LOGNAME_COM,
                "zipWriter_ exist\n");
        return MZ_OK;
    }

    zipWriter_ = mz_zip_writer_create();
    if(!zipWriter_) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOGNAME_COM,
                "create zipWriter_ failed\n");
        return MZ_MEM_ERROR;
    }
    
    return MZ_OK;
}
```

---

## [84/100] ID: CPP_0274 | C/C++ (T)
- Rule ID: `cppcheck/nullPointer`
- Target File: `br_proxy/br_proxy_server_manager.c`
- Warning: Possible null pointer dereference: nodeInfo

### Buggy Snippet
```cpp
static void ServerDeleteChannelByPid(pid_t callingPid)
{
    if (g_serverList == NULL) {
        TRANS_LOGD(TRANS_SVC, "[br_proxy] not init");
        return;
    }
    if (SoftBusMutexLock(&(g_serverList->lock)) != SOFTBUS_OK) {
        TRANS_LOGE(TRANS_SVC, "[br_proxy] lock failed");
        return;
    }
    ServerBrProxyChannelInfo *nodeInfo = NULL;
    ServerBrProxyChannelInfo *nodeNext = NULL;
    LIST_FOR_EACH_ENTRY_SAFE(nodeInfo, nodeNext, &(g_serverList->list), ServerBrProxyChannelInfo, node) {
        TRANS_LOGI(TRANS_SVC, "[br_proxy] by pid:%{public}d  pid:%{public}d",
            callingPid, nodeInfo->callingPid);
        if (nodeInfo->callingPid != callingPid) {
            continue;
        }
        ListDelete(&nodeInfo->node);
        SoftBusFree(nodeInfo);
        TransBrProxyRemoveObject(callingPid);
        g_serverList->cnt--;
        TRANS_LOGI(TRANS_SVC, "[br_proxy] by pid:%{public}d delete node success, cnt%{public}d",
            callingPid, g_serverList->cnt);
        break;
    }
    (void)SoftBusMutexUnlock(&(g_serverList->lock));
    return;
}
```

---

## [85/100] ID: CPP_0126 | C/C++ (T)
- Rule ID: `cppcheck/functionStatic`
- Target File: `socketio_tls/library/src/main/cpp/socketio_module_napi.cpp`
- Warning: Technically the member function 'ClientSocket::OnOpen' can be static (but you may consider moving to unnamed namespace).

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

---

## [86/100] ID: CPP_0237 | C/C++ (T)
- Rule ID: `cppcheck/nullPointer`
- Target File: `adapter/common/net/bluetooth/ble/softbus_adapter_ble_gatt_server.c`
- Warning: Possible null pointer dereference: it

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

---

## [87/100] ID: CPP_0139 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `spinec/Spinec/src/main/cpp/thirdparty/stb/stb_image.h`
- Warning: Condition 'g->transparent>=0' is always true

### Buggy Snippet
```cpp
for (;;) {
      int tag = stbi__get8(s);
      switch (tag) {
         case 0x2C: /* Image Descriptor */
         {
            stbi__int32 x, y, w, h;
            stbi_uc *o;

            x = stbi__get16le(s);
            y = stbi__get16le(s);
            w = stbi__get16le(s);
            h = stbi__get16le(s);
            if (((x + w) > (g->w)) || ((y + h) > (g->h)))
               return stbi__errpuc("bad Image Descriptor", "Corrupt GIF");

            g->line_size = g->w * 4;
            g->start_x = x * 4;
            g->start_y = y * g->line_size;
            g->max_x   = g->start_x + w * 4;
            g->max_y   = g->start_y + h * g->line_size;
            g->cur_x   = g->start_x;
            g->cur_y   = g->start_y;
            if (w == 0)
               g->cur_y = g->max_y;

            g->lflags = stbi__get8(s);

            if (g->lflags & 0x40) {
               g->step = 8 * g->line_size; // first interlaced spacing
               g->parse = 3;
            } else {
               g->step = g->line_size;
               g->parse = 0;
            }

            if (g->lflags & 0x80) {
               stbi__gif_parse_colortable(s,g->lpal, 2 << (g->lflags & 7), g->eflags & 0x01 ? g->transparent : -1);
               g->color_table = (stbi_uc *) g->lpal;
            } else if (g->flags & 0x80) {
               g->color_table = (stbi_uc *) g->pal;
            } else
               return stbi__errpuc("missing color table", "Corrupt GIF");

            o = stbi__process_gif_raster(s, g);
            if (!o) return NULL;
            pcount = g->w * g->h;
            if (first_frame && (g->bgindex > 0)) {
               for (pi = 0; pi < pcount; ++pi) {
                  if (g->history[pi] == 0) {
                     g->pal[g->bgindex][3] = 255; // just in case it was made transparent, undo that; It will be reset next frame if need be;
                     memcpy( &g->out[pi * 4], &g->pal[g->bgindex], 4 );
                  }
               }
            }

            return o;
         }

         case 0x21: // Comment Extension.
         {
            int len;
            int ext = stbi__get8(s);
            if (ext == 0xF9) { // Graphic Control Extension.
               len = stbi__get8(s);
               if (len == 4) {
                  g->eflags = stbi__get8(s);
                  g->delay = 10 * stbi__get16le(s); // delay - 1/100th of a second, saving as 1/1000ths.
                  if (g->transparent >= 0) {
                     g->pal[g->transparent][3] = 255;
                  }
                  if (g->eflags & 0x01) {
                     g->transparent = stbi__get8(s);
                     if (g->transparent >= 0) {
                        g->pal[g->transparent][3] = 0;
                     }
                  } else {
                     stbi__skip(s, 1);
                     g->transparent = -1;
                  }
               } else {
                  stbi__skip(s, len);
                  break;
               }
            }
            while ((len = stbi__get8(s)) != 0) {
               stbi__skip(s, len);
            }
            break;
         }

         case 0x3B: // gif stream termination code
            return (stbi_uc *) s; // using '1' causes warning on some compilers

         default:
            return stbi__errpuc("unknown code", "Corrupt GIF");
      }
   }
}
```

---

## [88/100] ID: CPP_0328 | C/C++ (T)
- Rule ID: `cppcheck/redundantAssignment`
- Target File: `services/media_assets_manager/src/service/media_assets_delete_service.cpp`
- Warning: Variable 'ret' is reassigned a value before the old one has been used.

### Buggy Snippet
```cpp
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
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

#define MLOG_TAG "Media_Service"

#include "media_assets_delete_service.h"

#include "media_log.h"
#include "medialibrary_type_const.h"
#include "medialibrary_db_const.h"
#include "medialibrary_album_fusion_utils.h"
#include "photos_po_writer.h"
#include "photo_file_operation.h"
#include "media_assets_service.h"
#include "media_assets_utils.h"
#include "medialibrary_asset_operations.h"
#include "lake_file_operations.h"
#include "dfx_utils.h"
#include "lake_file_utils.h"
#include "medialibrary_notify.h"
#include "medialibrary_photo_operations.h"
#include "thumbnail_service.h"

namespace OHOS::Media::Common {
int32_t MediaAssetsDeleteService::DeleteLocalAssets(const std::vector<std::string> &fileIds)
{
    // Ensure the process is single-threaded.
    std::lock_guard<std::mutex> lock(this->deleteAssetsMutex_);
    // Find assets info.
    std::vector<PhotosPo> photosList;
    int32_t ret = this->mediaAssetsDao_.QueryAssets(fileIds, photosList);
    CHECK_AND_RETURN_RET_LOG(
        ret == E_OK, ret, "QueryAssets fail, ret: %{public}d, fileIds: %{public}zu", ret, fileIds.size());
    // Aggreate all the target fileIds.
    std::vector<std::string> targetFileIds;
    // Handle the LOCAL_AND_CLOUD assets, provide the LOCAL copy.
    ret = this->BatchCopyAndMoveLocalAssetToTrash(photosList, targetFileIds);
    CHECK_AND_RETURN_RET_LOG(
        !targetFileIds.empty(), E_OK, "No need to handle, all are CLOUD. fileIds: %{public}zu", fileIds.size());
    // Move the assets to trash.
    ret = MediaAssetsService::GetInstance().TrashPhotos(targetFileIds);
    MEDIA_INFO_LOG("DeleteLocalAssets completed, ret: %{public}d, fileIds size: %{public}zu, "
                   "photosList: %{public}zu, targetFileIds: %{public}zu",
        ret,
        fileIds.size(),
        photosList.size(),
        targetFileIds.size());
    return ret;
}
```

---

## [89/100] ID: CPP_0353 | C/C++ (T)
- Rule ID: `cppcheck/redundantAssignment`
- Target File: `ijkplayer/src/main/cpp/ijkplayer/ff_ffplay.c`
- Warning: Variable 'is->max_frame_duration' is reassigned a value before the old one has been used.

### Buggy Snippet
```cpp
if (ffp->genpts)
        ic->flags |= AVFMT_FLAG_GENPTS;

    av_format_inject_global_side_data(ic);
    //
    //AVDictionary **opts;
    //int orig_nb_streams;
    //opts = setup_find_stream_info_opts(ic, ffp->codec_opts);
    //orig_nb_streams = ic->nb_streams;


    if (ffp->find_stream_info) {
        AVDictionary **opts = setup_find_stream_info_opts(ic, ffp->codec_opts);
        int orig_nb_streams = ic->nb_streams;

        do {
            if (av_stristart(is->filename, "data:", NULL) && orig_nb_streams > 0) {
                for (i = 0; i < orig_nb_streams; i++) {
                    if (!ic->streams[i] || !ic->streams[i]->codecpar || ic->streams[i]->codecpar->profile == FF_PROFILE_UNKNOWN) {
                        break;
                    }
                }

                if (i == orig_nb_streams) {
                    break;
                }
            }
            err = avformat_find_stream_info(ic, opts);
        } while(0);
        ffp_notify_msg1(ffp, FFP_MSG_FIND_STREAM_INFO);

        for (i = 0; i < orig_nb_streams; i++)
            av_dict_free(&opts[i]);
        av_freep(&opts);

        if (err < 0) {
            av_log(NULL, AV_LOG_WARNING,
                   "%s: could not find codec parameters\n", is->filename);
            ret = -1;
            goto fail;
        }
    }
    if (ic->pb)
        ic->pb->eof_reached = 0; // FIXME hack, ffplay maybe should not use avio_feof() to test for the end

    if (ffp->seek_by_bytes < 0)
        ffp->seek_by_bytes = !!(ic->iformat->flags & AVFMT_TS_DISCONT) && strcmp("ogg", ic->iformat->name);

    is->max_frame_duration = (ic->iformat->flags & AVFMT_TS_DISCONT) ? 10.0 : 3600.0;
    is->max_frame_duration = 10.0;
    av_log(ffp, AV_LOG_INFO, "max_frame_duration: %.3f\n", is->max_frame_duration);

#ifdef FFP_MERGE
    if (!window_title && (t = av_dict_get(ic->metadata, "title", NULL, 0)))
        window_title = av_asprintf("%s - %s", t->value, input_filename);

#endif
    /* if seeking requested, we execute it */
    if (ffp->start_time != AV_NOPTS_VALUE) {
        int64_t timestamp;

        timestamp = ffp->start_time;
        /* add the stream start time */
        if (ic->start_time != AV_NOPTS_VALUE)
            timestamp += ic->start_time;
        ret = avformat_seek_file(ic, -1, INT64_MIN, timestamp, INT64_MAX, 0);
        if (ret < 0) {
            av_log(NULL, AV_LOG_WARNING, "%s: could not seek to position %0.3f\n",
                    is->filename, (double)timestamp / AV_TIME_BASE);
        }
    }

    is->realtime = is_realtime(ic);

    av_dump_format(ic, 0, is->filename, 0);

    int video_stream_count = 0;
    int h264_stream_count = 0;
    int first_h264_stream = -1;
    for (i = 0; i < ic->nb_streams; i++) {
        AVStream *st = ic->streams[i];
        enum AVMediaType type = st->codecpar->codec_type;
        st->discard = AVDISCARD_ALL;
        if (type >= 0 && ffp->wanted_stream_spec[type] && st_index[type] == -1)
            if (avformat_match_stream_specifier(ic, st, ffp->wanted_stream_spec[type]) > 0)
                st_index[type] = i;

        // choose first h264

        if (type == AVMEDIA_TYPE_VIDEO) {
            enum AVCodecID codec_id = st->codecpar->codec_id;
            video_stream_count++;
            if (codec_id == AV_CODEC_ID_H264) {
                h264_stream_count++;
                if (first_h264_stream < 0)
                    first_h264_stream = i;
            }
        }
    }
```

---

## [90/100] ID: CPP_0286 | C/C++ (T)
- Rule ID: `cppcheck/memleak`
- Target File: `components/nstackx/nstackx_core/dfile/core/nstackx_file_manager.c`
- Warning: Memory leak: blockFrame

### Buggy Snippet
```cpp
static int32_t PushRecvBlockFrame(FileListTask *fileList, FileDataFrame *frame)
{
    BlockFrame *blockFrame = NULL;
    int32_t ret;
    uint8_t isRetran;

    blockFrame = (BlockFrame *)calloc(1, sizeof(BlockFrame));
    if (blockFrame == NULL) {
        DFILE_LOGE(TAG, "memory calloc failed");
        return FILE_MANAGER_ENOMEM;
    }
    blockFrame->fileDataFrame = frame;
    isRetran = frame->header.flag & NSTACKX_DFILE_DATA_FRAME_RETRAN_FLAG;
    if (isRetran) {
        ret = MutexListAddNode(&fileList->recvBlockList, &blockFrame->list, NSTACKX_TRUE);
    } else {
        ret = MutexListAddNode(&fileList->recvBlockList, &blockFrame->list, NSTACKX_FALSE);
    }
    if (ret != NSTACKX_EOK) {
        free(blockFrame);
        DFILE_LOGE(TAG, "add node to recv block list failed");
        return FILE_MANAGER_EMUTEX;
    }
    SemPost(&fileList->semStop);
    return FILE_MANAGER_EOK;
}
```

---

## [91/100] ID: CPP_0113 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `ohos_ssh/library/src/main/cpp/napi/ssh2_napi.cpp`
- Warning: Condition 'ssh2Napi' is always true

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

---

## [92/100] ID: CPP_0351 | C/C++ (T)
- Rule ID: `cppcheck/uninitvar`
- Target File: `library/src/main/cpp/napi/http2_common.h`
- Warning: Uninitialized variables: sendDataResult.wantIo, sendDataResult.fd, sendDataResult.writeBuffLen, sendDataResult.callbacks, sendDataResult.buffer

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

---

## [93/100] ID: CPP_0167 | C/C++ (T)
- Rule ID: `cppcheck/shadowVariable`
- Target File: `vap/vap_module/src/main/cpp/render/plugin_render.cpp`
- Warning: Local variable 'ret' shadows outer variable

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

---

## [94/100] ID: CPP_0029 | C/C++ (T)
- Rule ID: `cppcheck/passedByValue`
- Target File: `napi/settings/napi_settings.cpp`
- Warning: Function parameter 'tableName' should be passed by const reference.

### Buggy Snippet
```cpp
// get uri for stage model
std::string GetStageUriStr(std::string tableName, int id, std::string keyStr)
{
    if (id < USERID_HELPER_NUMBER) {
        id = USERID_HELPER_NUMBER;
    }
    std::string idStr = std::to_string(id);
    if (tableName == "global") {
        std::string retStr =
            "datashare:///com.ohos.settingsdata/entry/settingsdata/SETTINGSDATA?Proxy=true&key=" + keyStr;
        return retStr;
    } else if (tableName == "system") {
        std::string retStr = "datashare:///com.ohos.settingsdata/entry/settingsdata/USER_SETTINGSDATA_" + idStr +
                             "?Proxy=true&key=" + keyStr;
        return retStr;
    } else if (tableName == "secure") {
        std::string retStr = "datashare:///com.ohos.settingsdata/entry/settingsdata/USER_SETTINGSDATA_SECURE_" + idStr +
                             "?Proxy=true&key=" + keyStr;
        return retStr;
    } else {
        // return global uri
        std::string retStr =
            "datashare:///com.ohos.settingsdata/entry/settingsdata/SETTINGSDATA?Proxy=true&key=" + keyStr;
        return retStr;
    }
}
```

---

## [95/100] ID: CPP_0118 | C/C++ (T)
- Rule ID: `cppcheck/functionStatic`
- Target File: `socketio/library/src/main/cpp/socketio_module_napi.cpp`
- Warning: Technically the member function 'ClientSocket::OnOpen' can be static (but you may consider moving to unnamed namespace).

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
                               sio::message::list const &message, bool needAck, sio::message::list &ack_message)
    {
        g_isOnce = false;
        handler_event_listener_aux(context, name, message, needAck, ack_message);
    }

    void on_binary_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                                      sio::message::list const &message, bool needAck, sio::message::list &ack_message)
    {
        g_isOnce = false;
        handler_binary_event_listener_aux(context, name, message, needAck, ack_message);
    }

    void on_multi_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                                    sio::message::list const &message, bool needAck, sio::message::list &ack_message)
    {
        g_isOnce = false;
        handler_multi_event_listener_aux(context, name, message, needAck, ack_message);
    }

    void once_event_listener_aux(const OHOS::SocketIO::SocketIOContext &context, const std::string &name,
                                 sio::message::list const &message, bool needAck, sio::message::list &ack_message)
    {
        g_isOnce = true;
        handler_event_listener_aux(context, name, message, needAck, ack_message);
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
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, "LOG_TAG", "SOCKETIO_TAG_NAPI------>handler_message_json list.size = %{public}d", list.size());
        if (list.size() == 1) {
            str += "{";
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
            str += "}";
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

    void on_emit_callback(std::string const &ack_name, sio::message::list const &list)
    {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, "LOG_TAG", "SOCKETIO_TAG_NAPI------>on_emit_callback -------");
        napi_ref on_emit_listener_call_ref = on_emit_listener_call_ref_map[ack_name.c_str()];
        if (on_emit_listener_call_ref == nullptr) {
            OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, "on_emit_listener_call_ref is null");
            return;
        }
        std::string message_json;
        if (list.size() > 0) {
            message_json += handler_message_json(list);
        }
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, "LOG_TAG",
                     "SOCKETIO_TAG_NAPI------>on_emit_callback message_json = %{public}s", message_json.c_str());

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
            // 调用主线程函数，传入 Data
            napi_call_threadsafe_function(g_tsfnEmitBinaryCall, localBinaryInfo.release(), napi_tsfn_blocking);
        }
    }
};
```

---

## [96/100] ID: CPP_0017 | C/C++ (T)
- Rule ID: `cppcheck/passedByValue`
- Target File: `cj/settings/src/cj_settings.cpp`
- Warning: Function parameter 'setValue' should be passed by const reference.

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

---

## [97/100] ID: CPP_0162 | C/C++ (T)
- Rule ID: `cppcheck/variableScope`
- Target File: `unrar/library/src/main/cpp/unrar.cpp`
- Warning: The scope of the variable 'success' can be reduced.

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

---

## [98/100] ID: CPP_0206 | C/C++ (T)
- Rule ID: `cppcheck/variableScope`
- Target File: `services/implementation/src/device_manager_service_impl.cpp`
- Warning: The scope of the variable 'hmlEnable160M' can be reduced.

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

---

## [99/100] ID: CPP_0138 | C/C++ (T)
- Rule ID: `cppcheck/knownConditionTrueFalse`
- Target File: `spinec/Spinec/src/main/cpp/thirdparty/stb/stb_image.h`
- Warning: Condition 'len>128' is always true

### Buggy Snippet
```cpp
while ((nleft = pixelCount - count) > 0) {
      len = stbi__get8(s);
      if (len == 128) {
      } else if (len < 128) {
         len++;
         if (len > nleft) return 0; // corrupt data
         count += len;
         while (len) {
            *p = stbi__get8(s);
            p += 4;
            len--;
         }
      } else if (len > 128) {
         stbi_uc   val;
         len = 257 - len;
         if (len > nleft) return 0; // corrupt data
         val = stbi__get8(s);
         count += len;
         while (len) {
            *p = val;
            p += 4;
            len--;
         }
      }
   }

   return 1;
}
```

---

## [100/100] ID: CPP_0034 | C/C++ (T)
- Rule ID: `cppcheck/useStlAlgorithm`
- Target File: `napi/settings/napi_settings_observer.cpp`
- Warning: Consider using std::any_of algorithm instead of a raw loop.

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

---

