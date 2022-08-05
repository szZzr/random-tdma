# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from Utilities import save_file, load_file, plot
import Simulator

def example(rounds:int)->None:
    '''
    Run just one experiment with static message generation's possibility (0.5)
    and prints the results.
    :param rounds: Number of rounds.
    '''
    nodes = 8
    report = Simulator.run(rounds=rounds, possibility=0.5)
    print(f'\nAverage delayed messages per round: {report["delayed_messages"] / rounds} messages\n'
          f'Average delayed transmissions per round: {report["delayed_trans"] / rounds} messages\n'
          f'Average transmitted messages per packet: {report["transmitted"] / rounds}/4 messages\n'
          f'Average waiting nodes per round: {100 * (report["waiting"] / rounds) / nodes} %'
          f'Average waiting in queue: {report["average_waiting_time"]}')

def run_sampling(rounds:int)->dict:
    '''
    Conducts experiments with usage of different possibilities for
    messages generation. Return its result as a dictionary. The keys
    denote the rank of possibility for each experiment.
    :param rounds: Number of rounds for each experiment
    :return: Experiments results
    '''
    samples = {}
    max_p = 0.65
    p = 0.05
    while p<=max_p:
        report = Simulator.run(rounds=rounds, possibility=round(p,2))
        samples.update({p:report})
        p += 0.05
    return samples


def read_samples(samples:dict, rounds:int)->tuple:
    '''
    Take as inputs the results of some experiments and returns two list,
    one that includes the average throughput and the other one that consists
    the average channel delay
    :param samples: Results of experiments
    :param rounds: Number of rounds.
    :return:
    '''
    transmitted = [result['transmitted'] / rounds for result in samples.values()]
    # delayed = [result['delayed_messages'] / rounds for result in samples.values()]
    # delayed = [result['delivered']/ (8*rounds)  for result in samples.values()]
    delayed = [result["average_waiting_time"] for result in samples.values()]
    return transmitted, delayed


def samples_plot(samples:tuple)->None:
    '''
    Plotting the given results.
    :param samples: Results of experiments
    '''
    x,y = samples
    plot(x= x, y= y, xlabel='Throughput', ylabel='Delay', title='Random TDMA')


def test_samples(rounds)->tuple:
    '''
    Testing method.
    :param rounds: Number of rounds.
    :return: A tuple of lists with the Delay and Throuhghput.
    '''
    samples = run_sampling(rounds)
    x, y = read_samples(samples, rounds)
    print(f'Throughput: {x}\nDelay: {y}')
    return (x,y)


# SAVE AND LOAD RESULTS
def run_save_samples(rounds:int)->dict:
    results = run_sampling(rounds)
    save_file(data=results, path='./results1.pkl')
    return results

def load_samples(rounds)->tuple:
    samples = load_file('./results1.pkl')
    return read_samples(samples, rounds)

def load_plot(rounds:int):
    x,y = load_samples(rounds)
    plot(x= x, y= y, xlabel='Throughput', ylabel='Delay', title='Random TDMA')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rounds = 100000
    # example(rounds)
    # run_save_samples(rounds)
    # load_plot(rounds)
    samples = test_samples(rounds)
    samples_plot(samples)
