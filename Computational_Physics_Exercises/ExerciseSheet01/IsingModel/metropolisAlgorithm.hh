
using namespace std;

int flipDipole(int dipoleValue) // flip a dipole value
{
    if (dipoleValue == 1)
        return -1;

    if (dipoleValue == -1)
        return 1;
    else
    {
        cout << "\nERROR: dipole has unexpected value\n";
        return 2;
    }
}

void configurationPlot(vector<int> configuration) // output the current configuration
{
    int N = configuration.size();

    for (int i = 0; i < N; i++)
    {
        cout << configuration[i] << " ";
    }
    cout << "\n";
}

double configurationEnergy(vector<int> configuration, double J) // configuration energy of the ising chain in Joule
{
    int N = configuration.size();

    double sum = 0;
    double term = 0;

    for (int i = 0; i < N; i++) // go through the sum
    {
        if (i == N - 1) // boundary coundition
        {
            term = double(configuration[N - 1]) * double(configuration[0]);
        }
        else
        {
            term = double(configuration[i]) * double(configuration[i + 1]);
        }
        sum = sum + term;
    }
    // calculate energy from the sum with J = 1
    double energy = -J * sum; // configuration energy in Joule

    return energy;
}

double configurationProbability(vector<int> currentConfiguration, vector<int> trialConfiguration, double kT, double J) // probability of trial configuration to be accepted
{
    double currentEnergy = configurationEnergy(currentConfiguration, J);
    double trialEnergy = configurationEnergy(trialConfiguration, J);
    double deltaEnergy = trialEnergy - currentEnergy;
    double probability = exp(-deltaEnergy / kT);
    return probability;
}

vector<int> metropolisAlgorith(int N, int steps, double J, double kT, bool coldStart) // this algorithm calculates a valid ising chain of N elemets
{
    // declarations
    srand(time(NULL));                // seeding the rand() function with a new seed each time
    vector<int> currentConfiguration; // Ising chain: with current configuration
    vector<int> trialConfiguration;   // Ising chain: with trial configuration

    int dipole;
    int flipDipoleNo;     // the position of the dipole that will be flipped
    double currentEnergy; // energy of the current configuration
    double trialEnergy;   // energy of the trial configuration
    double r;             // random number between 0 and 1, determines if trial config is accepted
    double p;             // probability that trial configuration will be accepted

    // initial setup ising chain
    for (int i = 0; i < N; i++) // set dipoles randomly to 1 or -1
    {
        if (coldStart)
            dipole = 1;
        else
            dipole = (rand() % 2) * 2 - 1;

        currentConfiguration.push_back(dipole);
    }

    // generate trial configurations and decide to accept or deny

    for (int i = 0; i < steps; i++)
    {
        // set trial configuration to current configuration
        trialConfiguration = currentConfiguration;

        // 1b) pick one random dipole
        flipDipoleNo = rand() % 20;

        // flip the dipole
        trialConfiguration[flipDipoleNo] = flipDipole(trialConfiguration[flipDipoleNo]);

        // calculate probabiliy from the configurations via Energy
        p = configurationProbability(currentConfiguration, trialConfiguration, kT, J);

        // generate random number r between 0 and 1
        r = (double)rand() / (RAND_MAX);
        // decide if trial configuration is accepted
        if (p >= r)
        {
            // accept trial configuration
            currentConfiguration = trialConfiguration;
        }
        else
        {
            // dont accept trial configuration
        }
    }
    return currentConfiguration;
}