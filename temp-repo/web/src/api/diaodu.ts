import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/admin/diaodu/list',
    create = '/myapp/admin/diaodu/create',
    delete = '/myapp/admin/diaodu/delete',

}

const listApi = async (data: any) =>
    post<any>({ url: URL.list, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const createApi = async (data: any) =>
    post<any>({ url: URL.create, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (data: any) =>
    post<any>({ url: URL.delete, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
export { listApi, createApi,deleteApi};
