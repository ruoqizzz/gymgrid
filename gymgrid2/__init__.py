from gym.envs.registration import register

register(
    id='grid-world-v0',
    entry_point='gymgrid2.envs:GridWorld',
)


register(
    id='windy-grid-world-v0',
    entry_point='gymgrid2.envs:WindyGridWorld',
)


register(
    id='cliff-v0',
    entry_point='gymgrid2.envs:Cliff',
)

register(
    id='sample1-v0',
    entry_point='gymgrid2.envs:Sample1',
)

register(
    id='sample2-v0',
    entry_point='gymgrid2.envs:Sample2',
)
