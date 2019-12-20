from gym.envs.registration import register

register(
    id='grid-world-v0',
    entry_point='gymgird.envs:GridWorld',
)

register(
    id='cliff-v0',
    entry_point='gymgrid.envs:Cliff',
)

register(
    id='sample1-v0',
    entry_point='gymgrid.envs:Sample1',
)

register(
    id='sample2-v0',
    entry_point='gymgrid.envs:Sample2',
)