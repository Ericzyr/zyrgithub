#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Issue:
    """
    本类的属性和jira上各个项目的必填字段一一对应
    """

    ###发生概率--无规律复现
    customfield_10111 = '10112'
    #优先级----严重
    priority = '2'
    customfield_10601 = '请填写具体状态描述'
    labels = ['auto_report']
    # import config
    # labels.extend(config.labels)

    issuetype = 'Bug'

    summary = ''
    description = ''

    versions = ''
    components = ''
    fields = []

    def __init__(self, summary, description, versions, components):
        self.summary =summary
        self.description = description
        self.versions = versions
        self.components = components

        self.fields = {
            'summary': self.summary,

            'customfield_10111': {
                'id': self.customfield_10111
            },
            'priority': {
                'id': self.priority
            },
            'versions': [{
                'name': self.versions
            }],
            'description': self.description,
            'customfield_10601': self.customfield_10601,
            'labels': self.labels,
            'issuetype': {
                'name': self.issuetype
            },
            'components': [{
                'name': self.components
            }],
        }

    def __str__(self):
        s = ''
        for i in self.fields.iterkeys():
            s += str(i)+":\n" + str(self.fields[i]) + "\n\n"
        return s



class DEMETER(Issue):
    key = "DEMETER"

    def __init__(self, summary, description, versions, components, time = None):
        Issue.__init__(self, summary, description, versions, components)
        self.fields.update({
                'project': {
                    'key': 'DEMETER'
                },
                # EUI5.8
                'customfield_12801': [{'id': '13116'}],
                # 938子项目/CN-X4-50 Pro
                'customfield_12623': [{'id': '12763'}],
            })


class TPRJECT(Issue):
    key = "TPRJECT"

    def __init__(self, summary, description, versions, components, time = None):
        Issue.__init__(self, summary, description, versions, components)
        self.fields.update({
                'project': {
                    'key': 'TPRJECT'
                },
            })


class BRANCHUS(Issue):

    def __init__(self, summary, description, versions, components,  time = None):
        Issue.__init__(self, summary, description, versions, components)
        self.fields.update({
                'project': {
                    'key': 'BRANCHUS'
                },
                # 'customfield_12103': [{'id': '12023'}],
            })




class EOS(Issue):

    def __init__(self, summary, description, versions, components,  time = None):
        Issue.__init__(self, summary, description, versions, components)
        self.fields.update({
                'project': {
                    'key': 'EOS'
                },
                'customfield_12103': [{'id': '12023'}],
            })



class TVSHARE(Issue):
    def __init__(self, summary, description, versions, components, createapp, createrom):
        Issue.__init__(self, summary, description, versions, components)
        del self.fields['versions']

        self.fields.update({
            'project': {
                'key': "TVSHARE"
            },
            # 创建版本（APP）
            'customfield_12638': createapp,
            #创建版本（ROM）5.8.217T_dailybuild_1107
            'customfield_12639': createrom,
            # [12855]电视ROM测试
            'customfield_12640': {
                'id': '12855'
            },
            # TVSHARE机型  12868:国内_X4-50/X4-50 Pro_Mstar938
            'customfield_12641': [{
                'id': '12868'
            }],

        })



class HERACLES(Issue):
    def __init__(self, summary, description, versions, components,time = None):
        Issue.__init__(self, summary, description, versions, components)
        self.fields.update({
            'project': {
                'key': "HERACLES"
            },
            # subproject :Max4-70
            'customfield_12615': [{'id': '12755'}],
        })


class EUISIX(Issue):


    # todo 由于好多设备没有，无法判断后续添加
    def __init__(self, summary, description, versions, components, device,testType,testPhase):
        Issue.__init__(self, summary, description, versions, components)
        # 如果查不到相应的eui，默认为6.0
        if device.letvUI == '5.8':
            EUIID = '13116'
        elif device.letvUI == '5.9':
            EUIID = '16506'
        elif device.letvUI == '6.0':
            EUIID = '13004'
        else:
            EUIID = '13004'



        # 由于设备有限无法获取设备信息，故暂时没有的型号报bug 时不填写
        if device.getProjectName() == 'TV_928':
            subProject = 'customfield_15517'
            if device.buildModel == 'X4-55S':
                # Letv X3-50
                subProjectId = '17783'
            elif device.buildModel == 'Letv X3-55 Pro':
                # X3-55
                # todo 由于没有x3-55 PRO 暂时先归为x3-55
                subProjectId = '17781'
            platFormId = '17766'
        elif device.getProjectName() == 'TV_918':
            subProject = 'customfield_15516'
            platFormId = '17765'
            # Letv X3-43
            if device.buildModel=='Letv X3-43':
                subProjectId = '17777'
            #MTBF
            elif device.buildModel=='Letv S40 Air':
                subProjectId = '17775'
            elif device.buildModel=='Letv X50 Air':
                subProjectId = '17780'

        elif device.getProjectName() == 'TV_938soundbar':
            subProject = 'customfield_12623'
            platFormId = '17767'
            if device.buildModel == 'Max4-55':
                subProjectId = '15000'

        elif device.getProjectName() == 'TV_938':

            if device.buildDescription.find('x4m') != -1:
                platFormId = '17769'
            elif device.buildDescription.find('x4n') != -1:
                platFormId = '17768'
            else:
                platFormId = '17767'
            # 选择子项目
            subProject = 'customfield_12623'
            if device.buildModel == 'X4-55S':
                subProjectId = '16700'
            elif device.buildModel == 'X4-43N':
                subProjectId = '16913'
            elif device.buildModel == 'X4-50M' and device.buildDescription.find('x4m') != -1:
                subProject = '16342'
            elif device.buildModel == 'X4-50M' and device.buildDescription.find('x4m') == -1:
                subProject = '16339'
            elif device.buildModel == 'X4-55':
                subProjectId = '12879'
            elif device.buildModel == 'X4-43':
                subProjectId = '12765'

                #MTBF
            elif device.buildMode == 'X4-50':
                subProjectId = '12764'
            elif device.buildMode == 'X4-50Pro':
                subProjectId = '12763'
            elif device.buildMode == 'uMax85':
                subProjectId = '12880'
            elif device.buildMode == 'X4-40N':
                subProjectId = '16337'
            elif device.buildMode == 'X4-50N':
                subProjectId = '16339'
            elif device.buildMode == 'X4-40M':
                subProjectId = '16340'
            elif device.buildMode == 'X4-43M':
                subProjectId = '16341'
            elif device.buildMode == 'X4-55M':
                subProjectId = '16672'
            elif device.buildMode == 'X4-50SPro':
                subProjectId = '16673'
            elif device.buildMode == 'Unique55/65':
                subProjectId = '16676'
            elif device.buildMode == 'X4-40O':
                subProjectId = '16914'
            else :
                # subProject = None
                raise myException

        elif device.getProjectName() == 'TV_8064':
            # subProject = 'customfield_15519'
            # subProjectId = None
            platFormId = '17771'
        elif device.getProjectName() == 'TV_8094':
            subProject = 'customfield_15520'
            # Letv Max4-70
            subProjectId = '17799'
            platFormId = '17772'
        elif device.getProjectName() == 'TV_U4':
            platFormId = '17773'
            subProject = 'customfield_15521'
            subProjectId = '17800'

        self.fields.update({
            'project': {
                'key': "EUISIX"
            },
            # EUI5.5 13003 ,  EUI5.8 13116 ,  EUI5.9 16506 , EUI6.0 13004 ,Android TV M 13005,Android TV N 16507
            'customfield_12801': [{'id': EUIID}],
            # 测试类型 SmokeTest/冒烟测试 16766, 功能测试 16767，交互测试 16768，压力测试 16769，用户场景测试 16770，可恢复性测试 16771，性能测试 16772，稳定性测试 16773，兼容性测试 16774，认证测试 16775，MTBF 16776，IOT 16777，ET 16778，游戏测试 16779，外场测试 16780
            'customfield_15127': {'id': testType},
            # 测试阶段：主线测试 16781，交付测试 16782，维护测试 16783，开发分支测试 17802
            'customfield_15128': {'id': testPhase},
            # 开发平台：ALL 17764，918 17765，928 17766，938 17767，938CD 17768，938F 17769 ，948 17770，8064 17771，8094 17772，U4 17773
            'customfield_15515': [{'id': platFormId}],

            # 938子项目:CN-X4-40 12878，CN-X4-43 12765，CN-X4-43 Pro 13220，CN-X4-50 12764，CN-X4-50 Pro 12763，CN-X4-50 Pro NOFRC 13600，CN-X4-55 12879，CN-X4-55 curved 13017，CN-X4-65 13016，CN-X4-65 curved 13018，
            # CN-X65S 15300，CN-uMax85 12880，CN-uMax100 Laser 13711，CN-uMax120S 13019，CN-soundbar 15000，CN-Max55 Monitor 16000，CN-Max65 Monitor 16001，CN-X4-55 WCG 16100，CN-Max55 Wireless 16101，CN-Unique65 CES 16102，CN-uMax85Q 16103，US-X4-40 12901 ，US-X4-43 13008
            # US-X4-43 Pro 13606，US-X4-50 Pro 12902，US-X4-55 12903，US-X4-65 12904，US-uMax85 12906，US-uMax120S 12905，US-soundbar 16206，HK-X4-43 13006，HK-X4-43 Pro 13221，HK-X4-50 12917，HK-X4-50 Pro 13007，HK-X4-55 13604，HK-X4-65 13605，IN-X4-40 13244，IN-X4-43P 13245
            # IN-X4-50P 13246，IN-X4-55 13247，IN-X4-65 13248，Russia-X4-43P 14824，Russia-X4-55 14825，Russia-X4-65 14826，938-refactor 15001，CN_X4-40M(938) 16337，CN_X4-43M(938) 16338，CN_X4-50M(938) 16339，CN_X4-40M(938F) 16340，CN_X4-43M(938F)  16341，CN_X4-50M(938F) 16342
            # TCL55T1 16608 ，BleRemoteControl 16655，CN_X4-X55M（938） 16671，CN_X4-X55M（938F） 16672，CN_X4-X50S Pro（938F）16673，CN-Unique55/65 16676，CN-Unique75 16677，CN_X4_55S 16700，CN_X4_70 16701，CN-Max55 CD Monitor 16740，CN-Max65 CD Monitor 16741，CN_X4_75  16748，CN_X4-X55M生态版（938）16911，
            # CN_X4-X50M生态版（938） 16912，CN_X4-X43M生态版（938）16913，CN_X4-X40M生态版（938） 16914，Factory_IOD 16956，CN_X4-65M生态版（938） 17720
            subProject: [{'id': subProjectId}],

        })



# class XSEVEN(Issue):
#     def __init__(self, summary, description, versions, components, time):
#         Issue.__init__(self, summary, description, versions, components)
#         self.fields.update({
#             'project': {
#                 'key': "XSEVEN"
#             },
#             'customfield_13400': [{
#                 'value': 'X7_CN'
#             }],
#             'customfield_10984': [{
#                 'name': versions
#             }],
#             'customfield_12109': time,
#         })
#
#
# class RUBY(Issue):
#     def __init__(self, summary, description, versions, components, time):
#         Issue.__init__(self, summary, description, versions, components)
#         self.fields.update({
#             'project': {
#                 'key': "RUBY"
#             },
#             'customfield_12107': [{
#                 'value': '全网通'
#             }],
#             'customfield_12402': [{
#                 'value': '8996_X2'
#             }],
#             'customfield_12109': time,
#             # 影响版本
#             'customfield_10984': [{
#                 'name': versions
#             }],
#         })
#
#
# class LAFITE(Issue):
#     def __init__(self, summary, description, versions, components, time):
#         Issue.__init__(self, summary, description, versions, components)
#         self.fields.update({
#             'project': {
#                 'key': "LAFITE"
#             },
#             'customfield_12701': [{
#                 'value': '8976_S2_CN'
#             }],
#             'customfield_12109': time,
#             # 影响版本
#             'customfield_10984': [{
#                 'name': versions
#             }],
#         })
#
#
# class CORAL(Issue):
#     def __init__(self, summary, description, versions, components, time):
#         Issue.__init__(self, summary, description, versions, components)
#         self.fields.update({
#             'project': {
#                 'key': "CORAL"
#             },
#             'customfield_12107': [{
#                 'value': '全网通'
#             }],
#             'customfield_13024': [{
#                 'value': '8996_X10_FN'
#             }],
#             'customfield_12109': time,
#             # 影响版本
#             'customfield_10984': [{
#                 'name': versions
#             }],
#         })
#
#
# class XSIX(Issue):
#     def __init__(self, summary, description, versions, components, time):
#         Issue.__init__(self, summary, description, versions, components)
#         self.fields.update({
#             'project': {
#                 'key': "XSIX"
#             },
#             'customfield_12109': time,
#             # 影响版本
#             'customfield_10984': [{
#                 'name': versions
#             }],
#         })
#
#
# class CONNECT(Issue):
#     def __init__(self, summary, description, versions, components, time):
#         Issue.__init__(self, summary, description, versions, components)
#         self.fields.update({
#             'project': {
#                 'key': "CONNECT"
#             },
#             'customfield_12107': [{
#                 'value': '全网通'
#             }],
#             'customfield_12402': [{
#                 'value': '8996_ZL1'
#             }],
#             'customfield_12109': time,
#             # 影响版本
#             'customfield_10984': [{
#                 'name': versions
#             }],
#         })
#
#
# class MOSHARE(Issue):
#     def __init__(self, summary, description, versions, components, creatapp, phonename):
#         Issue.__init__(self, summary, description, versions, components)
#         del self.fields['versions']
#
#         # zl1需要报在connect库里，不分生不生态
#         modelMap = {
#             'X7': 'CN_X7_MTK6797',
#             'X10': 'CN_X10_MSM8996',
#             'X2': 'CN_X2_MSM8996',
#             'S2': 'CN_S2_MSM8976',
#             'X6': 'CN_X6_MTK6797',
#         }
#         self.fields.update({
#             'project': {
#                 'key': "MOSHARE"
#             },
#             'customfield_12611': [{
#                 'value': modelMap[phonename]
#             }],
#             # 12751[APP验收测试], 12752[手机ROM测试]
#             'customfield_12612': {
#                 'id': '12752'
#             },
#             'customfield_12613': [{
#                 # app version
#                 'name': creatapp
#             }],
#             'customfield_12614': [{
#                 # phone ROM version
#                 'name': versions
#             }],
#         })


class myException(Exception):
    print "子项目不存在"



if __name__ == '__main__':

    from jira import JIRA
    import config

    __url = config.url
    __user = config.user
    __pwd = config.pwd
    # 你可以通过访问下边的url获取某项目下报bug的所有字段
    # http://jira.letv.cn/rest/api/2/issue/createmeta?projectKeys=RUBY&issuetypeNames=Bug&expand=projects.issuetypes.fields
    myJira = JIRA(server=__url, basic_auth=(__user, __pwd))
    projectKey = 'EUISIX'
    meta = myJira.createmeta(projectKey, issuetypeNames="Bug", expand='projects.issuetypes.fields')
    fields = meta['projects'][0]['issuetypes'][0]['fields']
    for i in fields:
        # if fields[i]['required']:
        #     print i, " : ", fields[i]['name']
        if fields[i]:
            print i, " : ", fields[i]

