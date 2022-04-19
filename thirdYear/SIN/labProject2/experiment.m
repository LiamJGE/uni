#!/usr/bin/octave -qf
# Liam James Glennie England 
# Francesc Herrera Fernández

if (nargin != 3)
  printf("USage: ./experiment.m <data> <alphas> <bes>\n");
  exit(1);
end

arg_list = argv();
data = arg_list{1};
as = str2num(arg_list{2});
bs = str2num(arg_list{3});

load(data); 

[N, L] = size(data); 
D = L-1;
ll = unique(data(:,L));

rand("seed", 23);

data = data(randperm(N), :);
NTr = round(.7*N);
M = N - NTr;
te = data(N-M+1:N, :); # Testing set

# Header
printf("#      a       b   E   k Ete Ete (%%)    Ite (%%)\n");
printf("#------- ------- --- --- --- ------- ----------\n");

for a=as
  for b=bs
    [w, E, k] = perceptron(data(1:NTr,:), b, a);
    rl = zeros(M, 1);
    
    # Error estimation
    for m = 1:M # Iteramos por cada sample del test set
      tem = [1 te(m, 1:D)]'; # Feature vector de cada sample
      rl(m) = ll( linmach(w, tem) ); # Obtenemos la predicción para la clase del sample
    end

    [nerr m] = confus(te(:,L), rl); # nerr -> Ete
    m = nerr / M; # m -> Ete %

    s = sqrt(m*(1-m)/M); # Ite % se obtiene a partir de estas dos lineas
    r = 1.96*s;          #
    
    printf("%8.1f %7.1f %3d %3d %3d %7.1f [%2.1f, %2.1f]\n", a, b, E, k, nerr, m*100, (m-r)*100, (m+r)*100);
  end
end 