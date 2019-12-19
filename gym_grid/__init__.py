from gym.envs.registration import register

register(
    id='grid-world-v0',
    entry_point='gym_foo.envs:GridWorld',
)

register(
    id='cliff-v0',
    entry_point='gym_grid.envs:Cliff',
)

register(
    id='sample1-v0',
    entry_point='gym_grid.envs:Sample1',
)

register(
    id='sample2-v0',
    entry_point='gym_grid.envs:Sample2',
)