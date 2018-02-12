	           命令 "TVBOX_MemberLogin"://会员登录 参数 1 用户名 2密码
			   命令 "TVBOX_MemberLogOut"://会员登出
			   命令 "UI_PrintStep":  //向case.log中打印步骤信息 参数 1 文本
			   例子：
					,UI_PrintStep,Enter LeAccount
					,TVBOX_MemberLogin,13810131582,138101,
					,UI_PrintStep,logOut LeAccount
					,TVBOX_MemberLogOut,
	           
	           命令 "UI_SaveSelectedTextValueByResourceId"://根据ResourceId找到selected的文本并保存 参数 resource id
	           命令 "UI_SaveSelectedTextValueByClass"://根据ClassName android.widget.TextView找到selected的文本并保存 参数 Class Name
	           命令 "UI_SaveTextValueByResourceId"://根据ResourceId找到文本并保存 参数 resource id
	           命令 "UI_FindSavedTextByResourceId"://根据ResourceId找到文本并与保存的值进行比较 参数 resource id
	           命令 "UI_FindSavedTextNotEqualByResourceId"://根据ResourceId找到文本并与保存的值进行不相等比较 参数 resource id
			   例子：
					,UI_SaveSelectedTextValueByClass,android.widget.TextView,
					,RC_PressUp,2,
					,RC_PressDown,
					,UI_FindSavedTextByResourceId,com.letv.android.tv.letvlive:id/channel_number,
					,RC_PressUp,2,
					,RC_PressDown,
					,UI_SaveTextValueByResourceId,com.letv.android.tv.letvlive:id/channel_number,
					,RC_PressUp,2,
					,RC_PressDown,
					,UI_FindSavedTextByResourceId,com.letv.android.tv.letvlive:id/channel_number,
					,RC_PressUp,2,
					,RC_PressDown,
					,UI_UI_SaveSelectedTextValueByResourceId,com.letv.android.tv.letvlive:id/channel_number,
					,RC_PressUp,2,
					,RC_PressDown,,
					,UI_FindSaveTextNotEqualByResourceId,com.letv.android.tv.letvlive:id/channel_number,

	            命令 "UI_LeftMoveFindByText"://根据classname左移直到发现文本 参数1 class name 参数2 支持正则表达式的文本（例如 文本1|文本2）
				例子：
					,UI_LeftMoveFindByText,android.widget.TextView,标清,
					
	            命令 "UI_FindFolderAndEnterByText"://根据文本定位文件夹并进入 参数 支持正则表达式的文本（例如 文本1|文本2）
				例子：
					,UI_FindFolderAndEnterByText,内部存储,
	            命令 "UI_InputTextByEditTextClassAndIndex"://根据class android.widget.EditText序号输入文本 参数 1 序号 2 文本
				例子：
					,UI_InputTextByEditTextClassAndIndex,1，用户1,
				
	            命令 "UI_IsHighlightedByResourceIdAndIndex"://根据resource id和序号判断是否有焦点 参数 1 resource id 2 序号
				例子：
					,UI_IsHighlightedByResourceIdAndIndex,com.stv.filemanager:id/view_storage1,0,
					
	            命令 "UI_IsHighLightedByText"://文本定位的控件是否有焦点 参数 支持正则表达式的文本（例如 文本1|文本2）
				例子：
					,UI_IsHighLightedByText,暂时退出|退出,
				
	            命令 "UI_IsHighLightedByResourceId"://resource id定位的控件是否有焦点 参数 resource id
				例子：
					,UI_IsHighlightedByResourceIdAndIndex,com.stv.filemanager:id/view_storage,
				
	            命令 "UI_PackageNameNotEqual"://包名不等于 参数 包名
				例子：
					,UI_PackageNameNotEqual,com.stv.launcher,
	            
				命令 "UI_PackageNameEqual"://包名等于 参数 包名
				例子：
					,UI_PackageNameEqual,com.stv.launcher,
				
	            命令 "UI_NotFoundByResourceId"://指定resourceid的控件不存在 参数 resourceid
				例子：
					,UI_NotFoundByResourceId,com.stv.filemanager:id/layout_item1,
				
	            命令 "UI_NotFoundByText"://指定文本的控件不存在 参数 支持正则表达式的文本（例如 文本1|文本2）
				例子：
					,UI_NotFoundByText,已开启,
				
	            命令 "UI_GetChildrenCountByResourceId"://获得resource id指定的控件的子控件数量大于等于1 参数 resourceid
				例子：
					,UI_GetChildrenCountByResourceId,sina.mobile.tianqitongstv:id/life_index_layout,
				
	            命令 "UI_WaitTime"://等待时间 参数 秒
				例子：
					,UI_WaitTime,2,
					
	            命令 "UI_FindByResourceId"://根据resource id查找元素 参数 resource id
				例子：
					,UI_FindByResourceId,com.stv.globalsetting:id/picmode,
					
	            命令 "UI_FindAndClickByResourceId"://根据resource id查找元素并点击 参数 resource id
				例子：
					,UI_FindAndClickByResourceId,com.stv.globalsetting:id/picmode,
					
	            命令 "UI_FindByText":  //根据文本查找元素 参数 支持正则表达式的文本（例如 文本1|文本2）
				例子：
					,UI_FindByText,图像|image
					
	            命令 "UI_FindAndClickByText"://根据文本查找元素并点击 参数 支持正则表达式的文本（例如 文本1|文本2）
				例子：
					UI_FindAndClickByText,图像|image
					
	            命令 "UI_FindAndClickByTextCollection"://根据文本查找控件组并根据序号点击 参数 1支持正则表达式的文本（例如 文本1|文本2） 2序号
				例子：
					UI_FindAndClickByTextCollection,节目|channel,2
				
	            命令 "UI_InputTextByResourceId":  //根据resourceid 查找控件组输入文本 参数 1resourceid 2文本
				例子：
					,UI_InputTextByResourceId,com.stv.globalsetting:id/picmode,用户2

	            命令 "UI_GoToScreen":  //主页菜单跳转并验证跳转后焦点是否正确 参数 1 标题文本
				例子：
					,UI_PrintStep,enter live desktop
					,UI_GoToScreen,首页,
					,UI_PrintStep,enter application desktop
					,UI_GoToScreen,应用,
					,UI_PrintStep,enter leview desktop
					,UI_GoToScreen,乐见,
					,UI_PrintStep,enter signal desktop
					,UI_GoToScreen,信号源,
					
	            命令 "UI_LaunchApp":   //启动应用并验证启动后的包名 参数 应用名
				应用名如下：
				     GoogleSearch = "GoogleSearch|GoogleSearch";
					 TVlive = "TVlive|TVlive";
					 Channel = "Channel|Channel";
					 LeAccount = "乐视帐号|LeAccount|会员帐号";
					 Browser = "浏览器|Browser";
					 Filemanager = "文件管理|Filemanager";
					 Feedback = "问题反馈|Feedback";
					 Camera = "电视乐拍|Camera";
					 Settings = "设置|Settings";
					 SystemUpdate = "系统更新|SystemUpdate|Upgrade";
					 LeTv = "乐视视频|超级影视";
					 LeStore = "应用商店";
					 GameCenter = "超级游戏大厅";
					 HomeTime = "HomeTime";
					 Message = "消息";
					 Calendar = "日历";
					 Download = "下载中心";
					 TvManager = "电视管家";
					 LeSearch = "搜索";
					 Music = "音乐";
					 Help = "使用帮助";
					 Weather = "天气";
					 PlayHistory = "播放记录";
					 LeCloud = "云盘";
					 Inotice = "爱提醒";
					 LeSports = "超级体育";
					 Gallery = "相册";
					 Voice = "超级语音";
					 Shopping = "购物|大屏购物";
					 Golive = "同步院线";
					 Eco = "生态圈";
				例子:
					,UI_LaunchApp,日历
				
				
				
	            命令 "RC_PressBackDouble"://连击back键
				例子：
					,RC_PressBackDouble,,
				
	            命令 "RC_PressHome"://点击Home键 可选参数 次数
	            命令 "RC_PressRight"://点击右键 可选参数 次数
	            命令 "RC_PressLeft"://点击左键 可选参数 次数
	            命令 "RC_PressUp"://点击上键 可选参数 次数
	            命令 "RC_PressDown"://点击下键 可选参数 次数
	            命令 "RC_PressCenter"://点击中心键 可选参数 次数
	            命令 "RC_PressBack"://点击返回键 可选参数 次数
	            命令 "RC_PressSetting"://点击设置键 可选参数 次数
	            命令 "RC_PressMenu"://点击菜单键 可选参数 次数
	            命令 "RC_PressLe"://点击LE键 可选参数 次数
				例子：
					,RC_PressMenu,,
					,RC_PressHome,,
					,UI_WaitTime,5000,
					,RC_PressCenter,,
					,UI_WaitTime,500,
					,RC_PressDown,2,
					,UI_WaitTime,500,
