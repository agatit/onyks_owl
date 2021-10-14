// tslint:disable
/**
 * Onyks Wagon Location API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import { HttpMethods, QueryConfig, ResponseBody, ResponseText } from 'redux-query';
import * as runtime from '../runtime';
import {
    InstanceModule,
    InstanceModuleFromJSON,
    InstanceModuleToJSON,
    InstanceQueue,
    InstanceQueueFromJSON,
    InstanceQueueToJSON,
    ModuleParam,
    ModuleParamFromJSON,
    ModuleParamToJSON,
    QueueParam,
    QueueParamFromJSON,
    QueueParamToJSON,
} from '../models';

export interface CleanQueueRequest {
    projectId: string;
    instanceId: string;
}

export interface GetInstanceModuleRequest {
    projectId: string;
    instanceId: string;
    instanceModuleId: string;
}

export interface GetInstanceQueueRequest {
    projectId: string;
    instanceId: string;
}

export interface GetQueueCurrentImageRequest {
    projectId: string;
    instanceId: string;
}

export interface ListModuleParamsRequest {
    projectId: string;
    moduleId: string;
}

export interface ListQueueParamsRequest {
    projectId: string;
    queueId: string;
}

export interface ResetInstanceModuleRequest {
    projectId: string;
    instanceId: string;
    instanceModuleId: string;
}

export interface UpdateModuleParamRequest {
    projectId: string;
    moduleId: string;
    moduleParam?: ModuleParam;
}

export interface UpdateQueueParamRequest {
    projectId: string;
    queueId: string;
    queueParam?: QueueParam;
}


/**
 * Cleans queue
 */
function cleanQueueRaw<T>(requestParameters: CleanQueueRequest, requestConfig: runtime.TypedQueryConfig<T, number> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling cleanQueue.');
    }

    if (requestParameters.instanceId === null || requestParameters.instanceId === undefined) {
        throw new runtime.RequiredError('instanceId','Required parameter requestParameters.instanceId was null or undefined when calling cleanQueue.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/instance({instanceId})/queue(instanceQueueId)/clean`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"instanceId"}}`, encodeURIComponent(String(requestParameters.instanceId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'POST',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        throw "OH NO";
    }

    return config;
}

/**
* Cleans queue
*/
export function cleanQueue<T>(requestParameters: CleanQueueRequest, requestConfig?: runtime.TypedQueryConfig<T, number>): QueryConfig<T> {
    return cleanQueueRaw(requestParameters, requestConfig);
}

/**
 * Get list of instance modules
 */
function getInstanceModuleRaw<T>(requestParameters: GetInstanceModuleRequest, requestConfig: runtime.TypedQueryConfig<T, InstanceModule> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling getInstanceModule.');
    }

    if (requestParameters.instanceId === null || requestParameters.instanceId === undefined) {
        throw new runtime.RequiredError('instanceId','Required parameter requestParameters.instanceId was null or undefined when calling getInstanceModule.');
    }

    if (requestParameters.instanceModuleId === null || requestParameters.instanceModuleId === undefined) {
        throw new runtime.RequiredError('instanceModuleId','Required parameter requestParameters.instanceModuleId was null or undefined when calling getInstanceModule.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/instance({instanceId})/module({instanceModuleId})`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"instanceId"}}`, encodeURIComponent(String(requestParameters.instanceId))).replace(`{${"instanceModuleId"}}`, encodeURIComponent(String(requestParameters.instanceModuleId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'GET',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(InstanceModuleFromJSON(body), text);
    }

    return config;
}

/**
* Get list of instance modules
*/
export function getInstanceModule<T>(requestParameters: GetInstanceModuleRequest, requestConfig?: runtime.TypedQueryConfig<T, InstanceModule>): QueryConfig<T> {
    return getInstanceModuleRaw(requestParameters, requestConfig);
}

/**
 * Get list of instance queues
 */
function getInstanceQueueRaw<T>(requestParameters: GetInstanceQueueRequest, requestConfig: runtime.TypedQueryConfig<T, InstanceQueue> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling getInstanceQueue.');
    }

    if (requestParameters.instanceId === null || requestParameters.instanceId === undefined) {
        throw new runtime.RequiredError('instanceId','Required parameter requestParameters.instanceId was null or undefined when calling getInstanceQueue.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/instance({instanceId})/queue(instanceQueueId)`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"instanceId"}}`, encodeURIComponent(String(requestParameters.instanceId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'GET',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(InstanceQueueFromJSON(body), text);
    }

    return config;
}

/**
* Get list of instance queues
*/
export function getInstanceQueue<T>(requestParameters: GetInstanceQueueRequest, requestConfig?: runtime.TypedQueryConfig<T, InstanceQueue>): QueryConfig<T> {
    return getInstanceQueueRaw(requestParameters, requestConfig);
}

/**
 * Get list of instance queues
 */
function getQueueCurrentImageRaw<T>(requestParameters: GetQueueCurrentImageRequest, requestConfig: runtime.TypedQueryConfig<T, number> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling getQueueCurrentImage.');
    }

    if (requestParameters.instanceId === null || requestParameters.instanceId === undefined) {
        throw new runtime.RequiredError('instanceId','Required parameter requestParameters.instanceId was null or undefined when calling getQueueCurrentImage.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/instance({instanceId})/queue(instanceQueueId)/current_image`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"instanceId"}}`, encodeURIComponent(String(requestParameters.instanceId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'GET',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        throw "OH NO";
    }

    return config;
}

/**
* Get list of instance queues
*/
export function getQueueCurrentImage<T>(requestParameters: GetQueueCurrentImageRequest, requestConfig?: runtime.TypedQueryConfig<T, number>): QueryConfig<T> {
    return getQueueCurrentImageRaw(requestParameters, requestConfig);
}

/**
 * Get list of module params
 */
function listModuleParamsRaw<T>(requestParameters: ListModuleParamsRequest, requestConfig: runtime.TypedQueryConfig<T, Array<ModuleParam>> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling listModuleParams.');
    }

    if (requestParameters.moduleId === null || requestParameters.moduleId === undefined) {
        throw new runtime.RequiredError('moduleId','Required parameter requestParameters.moduleId was null or undefined when calling listModuleParams.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/module({moduleId})/param`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"moduleId"}}`, encodeURIComponent(String(requestParameters.moduleId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'GET',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(body.map(ModuleParamFromJSON), text);
    }

    return config;
}

/**
* Get list of module params
*/
export function listModuleParams<T>(requestParameters: ListModuleParamsRequest, requestConfig?: runtime.TypedQueryConfig<T, Array<ModuleParam>>): QueryConfig<T> {
    return listModuleParamsRaw(requestParameters, requestConfig);
}

/**
 * Get list of queue params
 */
function listQueueParamsRaw<T>(requestParameters: ListQueueParamsRequest, requestConfig: runtime.TypedQueryConfig<T, Array<QueueParam>> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling listQueueParams.');
    }

    if (requestParameters.queueId === null || requestParameters.queueId === undefined) {
        throw new runtime.RequiredError('queueId','Required parameter requestParameters.queueId was null or undefined when calling listQueueParams.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/queue({queueId})/param`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"queueId"}}`, encodeURIComponent(String(requestParameters.queueId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'GET',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(body.map(QueueParamFromJSON), text);
    }

    return config;
}

/**
* Get list of queue params
*/
export function listQueueParams<T>(requestParameters: ListQueueParamsRequest, requestConfig?: runtime.TypedQueryConfig<T, Array<QueueParam>>): QueryConfig<T> {
    return listQueueParamsRaw(requestParameters, requestConfig);
}

/**
 * Reset instance module
 */
function resetInstanceModuleRaw<T>(requestParameters: ResetInstanceModuleRequest, requestConfig: runtime.TypedQueryConfig<T, InstanceModule> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling resetInstanceModule.');
    }

    if (requestParameters.instanceId === null || requestParameters.instanceId === undefined) {
        throw new runtime.RequiredError('instanceId','Required parameter requestParameters.instanceId was null or undefined when calling resetInstanceModule.');
    }

    if (requestParameters.instanceModuleId === null || requestParameters.instanceModuleId === undefined) {
        throw new runtime.RequiredError('instanceModuleId','Required parameter requestParameters.instanceModuleId was null or undefined when calling resetInstanceModule.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/instance({instanceId})/module({instanceModuleId})/reset`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"instanceId"}}`, encodeURIComponent(String(requestParameters.instanceId))).replace(`{${"instanceModuleId"}}`, encodeURIComponent(String(requestParameters.instanceModuleId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'GET',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(InstanceModuleFromJSON(body), text);
    }

    return config;
}

/**
* Reset instance module
*/
export function resetInstanceModule<T>(requestParameters: ResetInstanceModuleRequest, requestConfig?: runtime.TypedQueryConfig<T, InstanceModule>): QueryConfig<T> {
    return resetInstanceModuleRaw(requestParameters, requestConfig);
}

/**
 * Updates module param
 */
function updateModuleParamRaw<T>(requestParameters: UpdateModuleParamRequest, requestConfig: runtime.TypedQueryConfig<T, ModuleParam> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling updateModuleParam.');
    }

    if (requestParameters.moduleId === null || requestParameters.moduleId === undefined) {
        throw new runtime.RequiredError('moduleId','Required parameter requestParameters.moduleId was null or undefined when calling updateModuleParam.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};

    headerParameters['Content-Type'] = 'application/json';


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/module({moduleId})/param`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"moduleId"}}`, encodeURIComponent(String(requestParameters.moduleId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'PUT',
            headers: headerParameters,
        },
        body: queryParameters || ModuleParamToJSON(requestParameters.moduleParam),
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(ModuleParamFromJSON(body), text);
    }

    return config;
}

/**
* Updates module param
*/
export function updateModuleParam<T>(requestParameters: UpdateModuleParamRequest, requestConfig?: runtime.TypedQueryConfig<T, ModuleParam>): QueryConfig<T> {
    return updateModuleParamRaw(requestParameters, requestConfig);
}

/**
 * Updates queue param
 */
function updateQueueParamRaw<T>(requestParameters: UpdateQueueParamRequest, requestConfig: runtime.TypedQueryConfig<T, QueueParam> = {}): QueryConfig<T> {
    if (requestParameters.projectId === null || requestParameters.projectId === undefined) {
        throw new runtime.RequiredError('projectId','Required parameter requestParameters.projectId was null or undefined when calling updateQueueParam.');
    }

    if (requestParameters.queueId === null || requestParameters.queueId === undefined) {
        throw new runtime.RequiredError('queueId','Required parameter requestParameters.queueId was null or undefined when calling updateQueueParam.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};

    headerParameters['Content-Type'] = 'application/json';


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/project({projectId})/queue({queueId})/param`.replace(`{${"projectId"}}`, encodeURIComponent(String(requestParameters.projectId))).replace(`{${"queueId"}}`, encodeURIComponent(String(requestParameters.queueId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'PUT',
            headers: headerParameters,
        },
        body: queryParameters || QueueParamToJSON(requestParameters.queueParam),
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(QueueParamFromJSON(body), text);
    }

    return config;
}

/**
* Updates queue param
*/
export function updateQueueParam<T>(requestParameters: UpdateQueueParamRequest, requestConfig?: runtime.TypedQueryConfig<T, QueueParam>): QueryConfig<T> {
    return updateQueueParamRaw(requestParameters, requestConfig);
}

