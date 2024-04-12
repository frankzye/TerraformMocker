provider "azurerm" {
  use_msi         = true
  client_id       = "00000000-0000-0000-0000-000000000000"
  tenant_id       = "10000000-0000-0000-0000-000000000000"
  subscription_id = "20000000-0000-0000-0000-000000000000"
  msi_endpoint    = "http://localhost:8080"
  features {}
}