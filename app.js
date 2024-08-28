// Configuration for AWS Cognito
const poolData = {
    UserPoolId: 'us-east-1_InNXWUZ3r', // Replace with your Cognito User Pool ID
    ClientId: '1oolfnel1sj152h9dlu3ii45sg' // Replace with your Cognito App Client ID
};

const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

// Handling form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails({
        Username: username,
        Password: password
    });

    const userData = {
        Username: username,
        Pool: userPool
    };

    const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function(result) {
            alert('Login successful!');
            const idToken = result.getIdToken().getJwtToken();
            console.log('ID Token: ' + idToken);
            // Redirect to another page or perform other actions
        },

        onFailure: function(err) {
            alert('Login failed: ' + err.message);
        }
    });
});
