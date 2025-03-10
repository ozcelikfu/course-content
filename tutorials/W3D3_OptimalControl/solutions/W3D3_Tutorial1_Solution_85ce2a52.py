
def run_policy(threshold, p_stay, low_rew_p, high_rew_p):
  """
  This function executes the policy (fully parameterized by the threshold) and
  returns two arrays:
    The sequence of actions taken from time 0 to T
    The sequence of rewards obtained from time 0 to T
  """
  params = [p_stay, low_rew_p, high_rew_p, threshold]
  binaryHMM_test = binaryHMM_belief(params, choose_policy="threshold")
  _, _, actions, rewards, _ = binaryHMM_test.generate_process()
  return actions, rewards


def get_optimal_threshold(p_stay, low_rew_p, high_rew_p, cost_sw):
  """
  Args:
    p_stay (float): probability of fish staying in their current location
    low_rew_p (float): probability of catching fish when you and the fist are in different locations.
    high_rew_p (float): probability of catching fish when you and the fist are in the same location.
    cost_sw (float): the cost of switching to the other location

  Returns:
    value (float): expected utility per unit time
  """
  global T
  T = 10000  # Setting a large time horizon
  get_randomness(T)

  # Create an array of 20 equally distanced candidate thresholds (min = 0., max=1.):
  threshold_array = np.linspace(0., 1., 20)

  # Using the function get_value() that you coded before and
  # the function run_policy() that we provide, compute the value of your
  # candidate thresholds:

  # Create an array to store the value of each of your candidates:
  value_array = np.zeros(len(threshold_array))

  for i in range(len(threshold_array)):
    actions, rewards = run_policy(threshold_array[i], p_stay, low_rew_p, high_rew_p)
    value_array[i] = get_value(rewards, actions, cost_sw)

  # Return the array of candidate thresholds and their respective values

  return threshold_array, value_array


# Feel free to change these parameters
stay_prob = .9
low_rew_prob = 0.1
high_rew_prob = 0.2
cost_sw = .1

# Visually determine the threshold that obtains the maximum utility
threshold_array, value_array = get_optimal_threshold(stay_prob, low_rew_prob, high_rew_prob, cost_sw)
with plt.xkcd():
  plot_value_threshold(threshold_array, value_array)