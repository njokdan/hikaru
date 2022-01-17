#
# Copyright (c) 2021 Incisive Technology Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
DO NOT EDIT THIS FILE!

This module is automatically generated using the Hikaru build program that turns
a Kubernetes swagger spec into the code for the hikaru.model package.
"""

from .v1beta1 import *


class Watchables(object):  # pragma: no cover
    """
    Attributes of this class are classes that support watches without the namespace
    keyword argument
    """
    MutatingWebhookConfigurationList = MutatingWebhookConfigurationList
    MutatingWebhookConfiguration = MutatingWebhookConfiguration
    ValidatingWebhookConfigurationList = ValidatingWebhookConfigurationList
    ValidatingWebhookConfiguration = ValidatingWebhookConfiguration
    CronJobList = CronJobList
    CronJob = CronJob
    CertificateSigningRequestList = CertificateSigningRequestList
    CertificateSigningRequest = CertificateSigningRequest
    LeaseList = LeaseList
    Lease = Lease
    EndpointSliceList = EndpointSliceList
    EndpointSlice = EndpointSlice
    EventList = EventList
    IngressClassList = IngressClassList
    IngressClass = IngressClass
    RuntimeClassList = RuntimeClassList
    RuntimeClass = RuntimeClass
    PodDisruptionBudgetList = PodDisruptionBudgetList
    PodDisruptionBudget = PodDisruptionBudget
    PodSecurityPolicyList = PodSecurityPolicyList
    PodSecurityPolicy = PodSecurityPolicy
    ClusterRoleBindingList = ClusterRoleBindingList
    ClusterRoleBinding = ClusterRoleBinding
    ClusterRoleList = ClusterRoleList
    ClusterRole = ClusterRole
    RoleBindingList = RoleBindingList
    RoleBinding = RoleBinding
    RoleList = RoleList
    Role = Role
    PriorityClassList = PriorityClassList
    PriorityClass = PriorityClass
    CSIDriverList = CSIDriverList
    CSIDriver = CSIDriver
    CSINodeList = CSINodeList
    CSINode = CSINode
    StorageClassList = StorageClassList
    StorageClass = StorageClass
    VolumeAttachmentList = VolumeAttachmentList
    VolumeAttachment = VolumeAttachment
    CustomResourceDefinitionList = CustomResourceDefinitionList
    CustomResourceDefinition = CustomResourceDefinition
    APIServiceList = APIServiceList
    APIService = APIService
    IngressList = IngressList
    Ingress = Ingress


watchables = Watchables


class NamespacedWatchables(object):  # pragma: no cover
    """
    Attributes of this class are classes that support watches with the namespace
    keyword argument
    """
    CronJobList = CronJobList
    LeaseList = LeaseList
    EndpointSliceList = EndpointSliceList
    EventList = EventList
    PodDisruptionBudgetList = PodDisruptionBudgetList
    RoleBindingList = RoleBindingList
    RoleList = RoleList
    IngressList = IngressList
    CronJob = CronJob
    Lease = Lease
    EndpointSlice = EndpointSlice
    PodDisruptionBudget = PodDisruptionBudget
    RoleBinding = RoleBinding
    Role = Role
    Ingress = Ingress


namespaced_watchables = NamespacedWatchables
