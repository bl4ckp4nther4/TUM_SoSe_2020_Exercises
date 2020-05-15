
using namespace std;

void configurationPlot2D(vector<vector<int>> configuration) // output the current configuration
{
    int N = configuration.size();

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < configuration[i].size(); j++)
        {
            cout << configuration[i][j] << " ";
        }
        cout << "\n";
    }
    cout << "\n";
}

double configurationEnergy2D(vector<vector<int>> configuration, double J) // configuration energy of the ising chain in Joule
{
    int N = configuration.size();
    int M = configuration[0].size();

    double sum = 0;
    double xTerm = 0;
    double yTerm = 0;

    for (int i = 0; i < N; i++) // go through the sum in x
    {
        for (int j = 0; j < M; j++) // go through the sum in y
        {

            // calculate the x term of the sum
            if (i == N - 1) // boundary coundition in x
                yTerm = double(configuration[N - 1][j]) * double(configuration[0][j]);

            else
                yTerm = double(configuration[i][j]) * double(configuration[i + 1][j]);

            // calculate the x term of the sum
            if (j == M - 1) // boundary coundition in x
                yTerm = double(configuration[i][M - 1]) * double(configuration[i][0]);

            else
                yTerm = double(configuration[i][j]) * double(configuration[i][j + 1]);

            sum = sum + xTerm + yTerm;
        }
    }

    // calculate energy from the sum with J = 1
    double energy = -J * sum; // configuration energy in Joule

    return sum;
}

double configurationProbability2D(vector<vector<int>> currentConfiguration, vector<vector<int>> trialConfiguration, double kT, double J) // probability of trial configuration to be accepted
{
    double currentEnergy = configurationEnergy2D(currentConfiguration, J);
    double trialEnergy = configurationEnergy2D(trialConfiguration, J);
    double deltaEnergy = trialEnergy - currentEnergy;
    double probability = exp(-deltaEnergy / kT);
    return probability;
}

vector<vector<int>> metropolisAlgorith2D(int N, int M, int steps, double J, double kT, bool coldStart) // this algorithm calculates a valid ising chain of N elemets
{
    // declarations
    srand(time(NULL));                                           // seeding the rand() function with a new seed each time
    vector<vector<int>> currentConfiguration(N, vector<int>(M)); // Ising chain: with current configuration
    vector<vector<int>> trialConfiguration(N, vector<int>(M));   // Ising chain: with trial configuration

    int dipole;
    int flipDipoleX;      // the x position of the dipole that will be flipped
    int flipDipoleY;      // the y position of the dipole that will be flipped
    double currentEnergy; // energy of the current configuration
    double trialEnergy;   // energy of the trial configuration
    double r;             // random number between 0 and 1, determines if trial config is accepted
    double p;             // probability that trial configuration will be accepted
    double E;

    // initial setup ising chain
    for (int i = 0; i < N; i++) // set dipoles randomly to 1 or -1
    {
        for (int j = 0; j < M; j++) // set dipoles randomly to 1 or -1
        {
            if (coldStart)
            {
                dipole = 1;
            }
            else
            {
                dipole = (rand() % 2) * 2 - 1;
            }
            currentConfiguration[i][j] = dipole;
        }
    }

    // generate trial configurations and decide to accept or deny
    for (int i = 0; i < steps; i++)
    {
        // set trial configuration to current configuration
        trialConfiguration = currentConfiguration;

        // 1b) pick one random dipole
        flipDipoleX = rand() % N;
        flipDipoleY = rand() % M;
        // flip the dipole
        trialConfiguration[flipDipoleX][flipDipoleY] = flipDipole(trialConfiguration[flipDipoleX][flipDipoleY]);

        // calculate probabiliy from the configurations via Energy
        p = configurationProbability2D(currentConfiguration, trialConfiguration, kT, J);

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