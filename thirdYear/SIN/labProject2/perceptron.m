function [w,E,k]=perceptron(data,b,a,K,iw)
  [N,L] = size(data);
  D = L-1;
  labs = unique(data(:,L));
  C = numel(labs);

  # Inicializa los argumentos
  if (nargin<5) w = zeros(D+1,C); else w=iw; end
  if (nargin<4) K = 200; end;
  if (nargin<3) a = 1.0; end;
  if (nargin<2) b = 0.1; end;

  for k=1:K
    E=0; # Contador de errores

    for n=1:N # Por cada sample
      xn = [1 data(n,1:D)]'; # Obtenemos feature vector
      cn = find(labs==data(n,L)); # Sacamos el label
      er = 0;                # Indica si se clasifica correctamente
      g = w(:,cn)'*xn;       # Clasificador 'verdadero'
      
      for c=1:C; # Itera por cada clase
        if (c != cn && w(:,c)' * xn + b > g) # Si se clasifica erroneamente
          w(:,c) = w(:,c) - a*xn; # Actualizamos pesos de la clase C
          er = 1; end; end # Señalamos el error
      
      if (er) # Si se ha encontrado algún error
        w(:,cn)=w(:,cn)+a*xn; E=E+1; end; end # Actualizamos los pesos de Cn
    if (E==0) break; end; end
endfunction