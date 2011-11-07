function p = predictOneVsAll(all_theta, X)
%PREDICT Predict whether the label is 0 or 1 using learned logistic 
%regression parameters all_theta
%   p = PREDICT(all_theta, X) computes the predictions for X using a 
%   threshold at 0.5 (i.e., if sigmoid(all_theta'*x) >= 0.5, predict 1)

m = size(X, 1);
num_labels = size(all_theta, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

% Add ones to the X data matrix
X = [ones(m, 1) X];

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned logistic regression parameters (one-vs-all).
%               You should set p to a vector of predictions (from 1 to
%               num_labels).
%
% Hint: This code can be done all vectorized using the max function.
%       In particular, the max function can also return the index of the 
%       max element, for more information see 'help max'. If your examples 
%       are in rows, then, you can use max(A, [], 2) to obtain the max 
%       for each row.
%       
for i=1:m,
    [x, p(i)] = max(sigmoid(all_theta * X(i,:)'));
end
% =========================================================================


end
