from specialistApp.models import Category
def get_menu_config():
    categories = []
    querysets = Category.objects.all()
    for q in querysets:
        dic={
            "name":q.ctg_name,
            "url":"/specialistApp/specialistmodel/?spe_ctg1__id="+str(q.id),
            'icon':'fas fa-plus-circle'
        }
        categories.append(dic)
    return {
        # 'system_keep': True,
        'dynamic': False,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
        'menus': [
            {
                'name': '全部考官信息',
                'icon': 'fas fa-address-card',
                'url': '/specialistApp/specialistmodel/',
            },
            {
                'name': '分类考官信息',
                'icon': 'fas fa-address-card',
                'models':categories
            },
            {
                'name': '分类信息',
                'icon': 'fas fa-list',
                'url': '/specialistApp/category/',
            },
            {
                'name': '随机抽取考官',
                'icon': 'fas fa-random',
                'url': 'select',

            },
            {
                'name':'考官数据管理',
                'icon':'fas fa-chart-bar',
                'url':'/select/statistic',
            },
            {
                'name':'根据随机数生成考官',
                'icon':'fas fa-random',
                'url':'select/upload',
            },
            {
                'name': '认证和授权',
                'icon': 'fas fa-shield-alt',
                'models': [
                    {
                        'name': '用户',
                        'icon': 'fas fa-user',
                        'url': '/auth/user/'
                    },
                    {
                        'name': '用户组',
                        'icon': 'fas fa-users',
                        'url': '/auth/group/'
                    },
                ]
            },

        ]
    }