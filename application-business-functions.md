# **Archimate Model Facts**
| Property | Value |
| ---- | ---- |
| **Model Name** | application-business-functions |
| **Model ID** | id-306bc760-438d-4cdf-b1ff-a11476e3dcd2 |

## <a name='id-df026a90-372e-4928-9940-3402a6cbe955'></a>Business Function: L1 Business Function
| Property | Value |
| ---- | ---- |
| **Name** | L1 Business Function |
| **Type** | Business Function |
| **Documentation** | Documentation for L1 business function.<br><br>Here is some further documentation. |
| **ID** | id-df026a90-372e-4928-9940-3402a6cbe955 |

## <a name='id-17d58b02-fdec-4b8b-a8b1-34e43632db5a'></a>Business Function: L2 Business Function
| Property | Value |
| ---- | ---- |
| **Name** | L2 Business Function |
| **Type** | Business Function |
| **Documentation** |  |
| **ID** | id-17d58b02-fdec-4b8b-a8b1-34e43632db5a |

| Relationship Type | Relationship Name | Target Name | Target Type | Relationship Documentation |
| ---- | ---- | ---- | ---- | ---- |
| Specialization |  | [L1 Business Function](#id-df026a90-372e-4928-9940-3402a6cbe955) | Business Function |  |
## <a name='id-31aac30e-236a-4c08-81da-3eb009204d4e'></a>Business Function: L3 Business Function
| Property | Value |
| ---- | ---- |
| **Name** | L3 Business Function |
| **Type** | Business Function |
| **Documentation** |  |
| **ID** | id-31aac30e-236a-4c08-81da-3eb009204d4e |

| Relationship Type | Relationship Name | Target Name | Target Type | Relationship Documentation |
| ---- | ---- | ---- | ---- | ---- |
| Specialization |  | [L2 Business Function](#id-17d58b02-fdec-4b8b-a8b1-34e43632db5a) | Business Function |  |
## <a name='id-52ae7cea-9110-4e0a-92f2-de50f02bcd13'></a>Application Component: Application 1
| Property | Value |
| ---- | ---- |
| **Name** | Application 1 |
| **Type** | Application Component |
| **Documentation** | First application.<br><br>Further documentation about first application. |
| **ID** | id-52ae7cea-9110-4e0a-92f2-de50f02bcd13 |

| Relationship Type | Relationship Name | Target Name | Target Type | Relationship Documentation |
| ---- | ---- | ---- | ---- | ---- |
| Realization | implements business function | [L1 Business Function](#id-df026a90-372e-4928-9940-3402a6cbe955) | Business Function | Application 1 implements the business function 'L1 Business Function'. |
## <a name='id-5a2f4550-b9d8-4cf1-9ef7-745392b4464e'></a>Application Component: Application 2
| Property | Value |
| ---- | ---- |
| **Name** | Application 2 |
| **Type** | Application Component |
| **Documentation** |  |
| **ID** | id-5a2f4550-b9d8-4cf1-9ef7-745392b4464e |

| Relationship Type | Relationship Name | Target Name | Target Type | Relationship Documentation |
| ---- | ---- | ---- | ---- | ---- |
| Realization |  | [L2 Business Function](#id-17d58b02-fdec-4b8b-a8b1-34e43632db5a) | Business Function |  |
## <a name='id-8ae75738-9c08-401c-8730-899893cc86b7'></a>Application Component: Application 3
| Property | Value |
| ---- | ---- |
| **Name** | Application 3 |
| **Type** | Application Component |
| **Documentation** |  |
| **ID** | id-8ae75738-9c08-401c-8730-899893cc86b7 |

| Relationship Type | Relationship Name | Target Name | Target Type | Relationship Documentation |
| ---- | ---- | ---- | ---- | ---- |
| Realization |  | [L2 Business Function](#id-17d58b02-fdec-4b8b-a8b1-34e43632db5a) | Business Function |  |
| Realization |  | [L3 Business Function](#id-31aac30e-236a-4c08-81da-3eb009204d4e) | Business Function |  |
