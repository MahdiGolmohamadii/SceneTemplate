import re

class SceneSetup(object):
    
    def __init__(self):
        self.templates = {}
        self.fetch_data()

    def fetch_data(self):
        #Fetch data from DB
        self.add_template('PN_LiI_Ma','Lighting', 'Maya', 'Lighting')
        self.add_template('PN_LiO_BL', 'Outerior Lighting', 'Blender', 'Lighting')
        self.add_template('PN_FX_HD', 'FX simulation', 'Houdini', 'FX')
        self.add_template('PN_MoP_MX', 'Props Modeling', 'Max', 'Modeling')
        self.add_template('PN_MoP_MA', 'Props Modeling', 'Maya', 'Modeling')
        self.add_template('PN_MoC_MA','Creature Modeling', 'Maya', 'Modeling')
        self.add_template('PN_MoC_MX','Creature Modeling', 'Max', 'Modeling')
        self.add_template('PN_RiH_MA','Human Rigging', 'Maya', 'Rig')
        self.add_template('PN_RiC_MA','Creature Rigging', 'Maya', 'Rig')
        self.add_template('PN_RiC_BL','Creature Rigging', 'Blender', 'Rig')
        self.add_template('PN_RiC_MX','Creature Rigging', 'Max', 'Rig')
        self.add_template('PN_Ani_MA', 'Animation', 'Maya', 'Animation')
        self.add_template('PN_Ani_BL', 'Animation', 'Blender', 'Animation')

    def add_template(self, code, name, software, category, source_path=''):
        temp = {
            code: {
            'name' : name,
            'software' : software,
            'category' : category,
            'Source_path' : source_path
            }
        }
        self.templates.update(temp)
    
    def print_templates(self):
        print(self.templates)
   
    def open_scene(self, code, dest):
        print('open scene: ' , code)
        print('Will copy {} from {} to {}'.format(code,self.templates[code]['Source_path'], dest))

    def search_in_templates(self, str=''):
        unsearchable=['Source_path']
        res = []
        str = '.*' + str + '.*'
        print(str)
        for tmp in self.templates:
            for item in self.templates[tmp].keys():
                if re.findall(str, self.templates[tmp][item]) and self.templates[tmp] not in unsearchable and tmp not in res:
                    res.append(tmp)
        return res
        
if __name__ == '__main__':
    sc = SceneSetup()
    print(sc.search_in_templates('r'))
    