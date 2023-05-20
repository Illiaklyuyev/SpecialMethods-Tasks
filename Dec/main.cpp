#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
using namespace std;

const double ALPHA=1.1;
const double BETA=1.0/ALPHA;
const double INITIAL_STEP=0.1;
const double MIN_STEP=1e-4;
const int MAX_EVALS=1000000;
const double MAX_VALUE=1e6;
const double INITIAL_VALUES=0;
const int PEAKS_AMOUNT=3;
const int PERTUBATION_INDEX=50;

vector<double> spectrum_instrument;
vector<double> spectrum_measured;


vector<double> vector_double_filled(int size, double value)
{
    vector<double> v={};
    for(int i=0;i<size;i++)
    {
        v.push_back(value);
    }
    return v;
}

vector<int> vector_int_filled(int size, int value)
{
    vector<int> v={};
    for(int i=0;i<size;i++)
    {
        v.push_back(value);
    }
    return v;
}


vector<double> read_points(string filename)
{
   ifstream fin(filename);
   double x,y;
   vector<double> points={};
   while (fin>>x>>y)
   {
       points.push_back(y);
   }
   return points;
}

void print_points(vector<double> points)
{
    for(int i=0;i<points.size();i++)
    {
        cout<<points[i]<<" ";
    }
    cout<<endl;
}

void write_result_points(string filename, vector<double> points)
{
    ofstream fout(filename);
    for (int i=0;i<points.size();i++)
    {
        fout<<points[i]<<endl;
    }
}

double calc_delta(vector<double> spectrum_convolved)
{
    double sum=0;
    for (int i=0;i<spectrum_measured.size();i++)
    {
        double delta=spectrum_measured[i]-spectrum_convolved[i];
        sum+=delta*delta;
    }
    return sqrt(sum);

}

vector<double> convolve(vector<double> spectrum_original)
{
    int points_instrument_size=spectrum_instrument.size();
    int points_original_size=spectrum_original.size();
    vector<double> points_convolved={};
    for (int i=0;i<points_original_size;i++)
    {
        double point_convolved=0;
        for (int j=0;j<points_instrument_size;j++)
        {
            int d= j-points_instrument_size/2;
            int pii=j;
            int psi=i-d;
            bool pii_in_range=0<=pii && pii<points_instrument_size;
            bool psi_in_range=0<=psi && psi<points_original_size;
            if (pii_in_range && psi_in_range)
            {
                point_convolved+=spectrum_instrument[pii]*spectrum_original[psi];
            }
        }
        points_convolved.push_back(point_convolved);
    }
    return points_convolved;
}

double calc_fit_residue(vector<double> spectrum_original)
{
    return calc_delta(convolve(spectrum_original));
}

class FitResult
{
public:
    string error_message;
    vector<double> params;
    double fit_residue;
    int fit_residue_evals;
    FitResult(string error_message):error_message(error_message){}
    FitResult(vector<double> params,double fit_residue,int fit_residue_evals):
        params(params),
        fit_residue(fit_residue),
        fit_residue_evals(fit_residue_evals){}
    static FitResult error(string error_message){
        return FitResult(error_message);
    }
};

bool is_params_ok(vector<double> params)
{
    int peaks_amount=0;
    for(int i=0;i<params.size();i++)
    {
        if(params[i]<0)
        {
            return false;
        }
        else
        {
            if(1<=i && i<params.size()-1)
            {
                if(params[i]>params[i-1] && params[i]>params[i+1])
                {
                    peaks_amount++;
                }
            }
        }
    }
    if(peaks_amount>PEAKS_AMOUNT)
    {
        return false;
    }
    return true;
}

int calc_index_of_best(vector<double> values,double prev_best) //?
{
    int index_of_best=-1;
    for(int i=0;i<values.size();i++)
    {
       if(values[i]<=prev_best && isfinite(values[i]))
       {
           index_of_best=i;
       }
    }
    return index_of_best;
}

FitResult find_spectrum_original_by_hooke_jeeves_method()
{ 
    int params_size=spectrum_measured.size();
    if (params_size==0)
    {
        return FitResult::error("Too few parameters");
    }
    //params is spectrum_original
    vector<double> params=vector_double_filled(params_size, INITIAL_VALUES);
    if(PERTUBATION_INDEX>=0)
    {
        params[PERTUBATION_INDEX]+=INITIAL_STEP;
    }
//    cout<<"params.size()= "<<params.size()<<endl;
    int fit_residue_evals=0;
    double residue_now=calc_fit_residue(params);
    fit_residue_evals++;
    if (!isfinite(residue_now))
    {
        return FitResult::error("residue_now isn't finite");
    }

    if(residue_now>=MAX_VALUE)
    {
        return FitResult::error("residue_now is too big");
    }
    double step=INITIAL_STEP;
    int iter=0;
    while(step>MIN_STEP && fit_residue_evals<MAX_EVALS)
    {
        iter++;
//        cout<<"iter "<<iter<<":"<<endl;
//        cout<<"step = "<<step<<endl;
//        cout<<"params@1 = ";
       // print_points(params);
        vector<double> residues_at_new_params={};
        for(int i=0;i<2*params_size;i++)
        {
            double delta = i%2==0 ? -step : step;
            double param_new=params[i/2]+delta;
            vector<double> params_new={};
            params_new.insert(params_new.begin(),params.begin(), params.end());
            params_new[i/2]=param_new;
            if(!isfinite(param_new) || !is_params_ok(params_new))
            {
                residues_at_new_params.push_back(NAN);
            }
            else
            {
                double residue=calc_fit_residue(params_new);
                fit_residue_evals++;
                residues_at_new_params.push_back(
                    isfinite(residue) ? residue : NAN
                );
            }
        }
//        cout<<"residues_at_new_params = ";
       // print_points(residues_at_new_params);
//        cout<<"residues_at_new_params = ";
      //  print_points(residues_at_new_params);
//        cout<<"residue_now = "<<residue_now<<endl;
        int index_of_best=calc_index_of_best(residues_at_new_params,residue_now);
//        cout<<"index_of_best = "<<index_of_best<<endl;
        if(index_of_best==-1)
        {
            step*=BETA;
        }
        else
        {
            double delta = index_of_best%2==0 ? -step : step;
            params[index_of_best/2]+=delta;
           // cout<<"params@2 = ";
          //  print_points(params);
            residue_now=residues_at_new_params[index_of_best];
            if (!isfinite(residue_now))
            {
                return FitResult::error("residue_now isn't finite");
            }
            step*=ALPHA;
        }
    }
    if(fit_residue_evals>=MAX_EVALS)
    {
        return FitResult::error("too many iterations");
    }
    return FitResult(params, residue_now, fit_residue_evals);
}

const double TO_NORMALIZE=10.0;
vector<double> normalize(vector<double> points)
{
    double maximum=0;
    for(int i=0;i<points.size();i++)
    {
        if(points[i]>maximum)
        {
            maximum=points[i];
        }
    }
    double k=TO_NORMALIZE/maximum;
    for(int i=0;i<points.size();i++)
    {
        points[i]*=k;
    }
    return points;
}

int main()
{
    spectrum_instrument=read_points("D:\\project\\Dec\\data\\inst0.dat");
    cout<<"spectrum_instrument.size= "<< spectrum_instrument.size()<<endl;
    spectrum_measured=read_points("D:\\project\\Dec\\data\\data0.dat");
    cout<<"spectrum_measured.size= "<< spectrum_measured.size()<<endl;
    FitResult fit_result=find_spectrum_original_by_hooke_jeeves_method();
    if(fit_result.error_message!="")
    {
        cout<<"error: "<<fit_result.error_message<<endl;
    }
    else
    {
        cout<<"fit_residue = "<<fit_result.fit_residue<<endl;
        cout<<"fit_residue_evals = "<<fit_result.fit_residue_evals<<endl;
        cout<<"fit_result.params.size()= "<<fit_result.params.size()<<endl;
        fit_result.params=normalize(fit_result.params);
        cout<<"fit_result.params = ";
        print_points(fit_result.params);
        write_result_points("D:\\project\\Dec\\data\\results.dat", fit_result.params);
    }
    cout<<"FINISHED"<<endl;
}
