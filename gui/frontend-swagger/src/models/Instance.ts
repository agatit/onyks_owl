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

import { exists, mapValues } from '../runtime';
import {
    Project,
    ProjectFromJSON,
    ProjectToJSON,
} from './';

/**
 * 
 * @export
 * @interface Instance
 */
export interface Instance  {
    /**
     * 
     * @type {string}
     * @memberof Instance
     */
    id?: string;
    /**
     * 
     * @type {Project}
     * @memberof Instance
     */
    project?: Project;
}

export function InstanceFromJSON(json: any): Instance {
    return {
        'id': !exists(json, 'id') ? undefined : json['id'],
        'project': !exists(json, 'project') ? undefined : ProjectFromJSON(json['project']),
    };
}

export function InstanceToJSON(value?: Instance): any {
    if (value === undefined) {
        return undefined;
    }
    return {
        'id': value.id,
        'project': ProjectToJSON(value.project),
    };
}


