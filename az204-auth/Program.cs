// See https://aka.ms/new-console-template for more information
using System;
using System.Threading.Tasks;
using Microsoft.Identity.Client;

namespace az204_auth {
    class Program {
        private const string _clientID = "55e15151-8c6e-43b4-945c-fef69dfeec7d";
        private const string _tenantId = "84ff045a-49f1-457c-856f-98ea50ccee00";
        public static async Task Main(string[] args) {
            var app = PublicClientApplicationBuilder
                .Create(_clientID)
                .WithAuthority(AzureCloudInstance.AzurePublic, _tenantId)
                .WithRedirectUri("http://localhost")
                .Build();
            string[] scopes = { "user.read" };
            AuthenticationResult result = await app.AcquireTokenInteractive(scopes).ExecuteAsync();

            Console.WriteLine($"Token:\t{result.AccessToken}");
        }
    }
}