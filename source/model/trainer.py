class Trainer(object):
    def __init__(self, agent_creator, env_creator):
        pass

    def train(self):
        for i in range(15000):
            memory = list(self.pool.prev_memory_states)
            rollout_obs, rollout_actions, rollout_rewards, rollout_mask = self.pool.interact()
            self.train_on_rollout(rollout_obs, rollout_actions, rollout_rewards, rollout_mask, memory)
