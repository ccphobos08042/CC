import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/admin/baoxiu/list',
    create = '/myapp/admin/baoxiu/create',
    update = '/myapp/admin/baoxiu/update',
    delete = '/myapp/admin/baoxiu/delete',

    jjupdate = '/myapp/admin/jingju/update',
    jjlist='/myapp/admin/jingju/list',
}

const listApi = async (params: any) => get<any>({ url: URL.list, params: params, data: {}, headers: {} });
const jjlistApi = async (params: any) => get<any>({ url: URL.jjlist, params: params, data: {}, headers: {} });
const createApi = async (data: any) =>
    post<any>({ url: URL.create, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const updateApi = async (params: any, data: any) =>
    post<any>({ url: URL.update, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (params: any) => post<any>({ url: URL.delete, params: params, headers: {} });
const jjupdateApi = async (params: any, data: any) =>
    post<any>({ url: URL.jjupdate, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
export { listApi, createApi, updateApi, deleteApi ,jjupdateApi,jjlistApi};
