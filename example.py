from rs_arch import main as rs

rs.KnowledgeBase.load('kb.json')
goal = rs.Goal()
goal.add_collection('Green Gobbo Goodies I')
goal.add_collection('Green Gobbo Goodies I')
goal.add_collection('Green Gobbo Goodies I')
goal.add_collection('Green Gobbo Goodies I')
material_storage = rs.MaterialStorage()
material_storage.add_batch(
    {
        ('Leather scraps', 100),
        ('White oak', 100),
        ('Warforged bronze', 100),
        ('Malachite green', 100),
    }
)
print(goal.get_materials_needed(material_storage))

# [('Leather scraps', 4), ('Weapon poison (3)', 4), ('Malachite green', 68),
# ('Samite silk', 80), ('Vellum', 96), ("Yu'biusk clay", 152), ('Mark of the
# Kyzaj', 192), ('Vulcanised rubber', 472)]
