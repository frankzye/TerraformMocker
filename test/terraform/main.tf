resource "azurerm_linux_virtual_machine_scale_set" "vmss" {
  location             = "eastasia"
  name                 = "test_vmss"
  resource_group_name  = "rg"
  admin_username       = "admin"
  instances            = 2
  computer_name_prefix = "vmss"
  sku                  = "Standard_F2s_v2"
  admin_password       = "asdf"
  source_image_id      = "/subscriptions/291bba3f-e0a5-47bc-a099-3bdcb2a50a05/resourceGroups/myResourceGroup/providers/Microsoft.Compute/images/Redhat9"
  network_interface {
    name = "nic"
    ip_configuration {
      name      = "ip"
      subnet_id = "/subscriptions/291bba3f-e0a5-47bc-a099-3bdcb2a50a05/resourceGroups/subnet-test/providers/Microsoft.Network/virtualNetworks/vnetname/subnets/subnet1"
    }
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
}